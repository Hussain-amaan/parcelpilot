import re

from app.data.queries import (
    get_order,
    get_account,
)

from app.tools.data_tools import (
    check_cancellation,
    check_service_credit,
    lookup_ticket,
    lookup_account,
    lookup_orders,
)

from app.tools.document_tools import (
    search_parcelpilot_documents,
)

from app.tickets.decision import (
    analyze_ticket_decision,
)

from app.agent.action_manager import (
    prepare_escalation,
)


def extract_order_id(query):
    """
    Extract an order ID such as ORD-1001.
    """

    match = re.search(
        r"\bORD-\d+\b",
        query.upper(),
    )

    return match.group(0) if match else None


def extract_ticket_id(query):
    """
    Extract a ticket ID such as TKT-501.
    """

    match = re.search(
        r"\bTKT-\d+\b",
        query.upper(),
    )

    return match.group(0) if match else None


def extract_account_id(query):
    """
    Extract an account ID such as ACCT-001.
    """

    match = re.search(
        r"\bACCT-\d+\b",
        query.upper(),
    )

    return match.group(0) if match else None


def detect_intent(query):
    """
    Lightweight deterministic intent detection.
    """

    text = query.lower()

    if any(
        word in text
        for word in [
            "cancel",
            "cancellation",
        ]
    ):
        return "cancellation"

    if any(
        word in text
        for word in [
            "credit",
            "compensation",
            "service credit",
        ]
    ):
        return "service_credit"

    if any(
        word in text
        for word in [
            "escalate",
            "escalation",
        ]
    ):
        return "escalation"

    if (
        "sla" in text
        or "severity" in text
        or "ticket" in text
        or "issue" in text
    ):
        return "ticket"

    return "document_search"


def handle_chat_query(
    query,
    account_id=None,
    assessment_time="16-08-2026 10:50",
):
    """
    Route a natural-language customer/support query
    to the appropriate deterministic tool.

    This router does not make policy decisions.
    """

    intent = detect_intent(query)

    order_id = extract_order_id(query)
    ticket_id = extract_ticket_id(query)

    # --------------------------------------------------
    # CANCELLATION
    # --------------------------------------------------

    if intent == "cancellation":

        if not order_id:
            return {
                "intent": intent,
                "status": "needs_information",
                "message": (
                    "Please provide the order ID "
                    "you want to check."
                ),
            }

        order = get_order(order_id)

        if order is None:
            return {
                "intent": intent,
                "status": "not_found",
                "message": (
                    f"Order {order_id} was not found."
                ),
            }

        order_account_id = order["account_id"]

        # Customer-facing access control.
        if (
            account_id is not None
            and order_account_id != account_id
        ):
            return {
                "intent": intent,
                "status": "access_denied",
                "message": (
                    "You are not authorised to access "
                    "this order."
                ),
            }

        account = get_account(
            order_account_id
        )

        result = check_cancellation(
            order=order,
            account=account,
            reference_time=assessment_time,
        )

        return {
            "intent": intent,
            "status": "success",
            "order_id": order_id,
            "result": result,
        }

    # --------------------------------------------------
    # SERVICE CREDIT
    # --------------------------------------------------

    if intent == "service_credit":

        if not order_id:
            return {
                "intent": intent,
                "status": "needs_information",
                "message": (
                    "Please provide the order ID "
                    "for the pickup issue."
                ),
            }

        order = get_order(order_id)

        if order is None:
            return {
                "intent": intent,
                "status": "not_found",
                "message": (
                    f"Order {order_id} was not found."
                ),
            }

        order_account_id = order["account_id"]

        if (
            account_id is not None
            and order_account_id != account_id
        ):
            return {
                "intent": intent,
                "status": "access_denied",
                "message": (
                    "You are not authorised to access "
                    "this order."
                ),
            }

        account = get_account(
            order_account_id
        )

        # Try to identify hours late.
        hours_match = re.search(
            r"(\d+(?:\.\d+)?)\s*hours?\s*late",
            query.lower(),
        )

        if not hours_match:
            return {
                "intent": intent,
                "status": "needs_information",
                "message": (
                    "Please specify how many hours "
                    "late the pickup is."
                ),
            }

        hours_late = float(
            hours_match.group(1)
        )

        carrier_fault = (
            "carrier fault" in query.lower()
            or "carrier fault is confirmed"
            in query.lower()
        )

        customer_fault = (
            "customer fault" in query.lower()
            or "customer-caused" in query.lower()
        )

        result = check_service_credit(
            order=order,
            account=account,
            hours_late=hours_late,
            carrier_fault=carrier_fault,
            customer_fault=customer_fault,
        )

        return {
            "intent": intent,
            "status": "success",
            "order_id": order_id,
            "result": result,
        }

    # --------------------------------------------------
    # TICKET / SLA
    # --------------------------------------------------

    if intent == "ticket":

        if not ticket_id:
            return {
                "intent": intent,
                "status": "needs_information",
                "message": (
                    "Please provide the ticket ID "
                    "you want me to investigate."
                ),
            }

        ticket_lookup = lookup_ticket(
            ticket_id
        )

        if not ticket_lookup["found"]:
            return {
                "intent": intent,
                "status": "not_found",
                "message": (
                    f"Ticket {ticket_id} was not found."
                ),
            }

        ticket = ticket_lookup["ticket"]

        # Access control.
        if (
            account_id is not None
            and ticket["account_id"] != account_id
        ):
            return {
                "intent": intent,
                "status": "access_denied",
                "message": (
                    "You are not authorised to access "
                    "this ticket."
                ),
            }

        decision = analyze_ticket_decision(
            ticket_id=ticket_id,
            assessment_time=assessment_time,
        )

        return {
            "intent": intent,
            "status": "success",
            "ticket_id": ticket_id,
            "decision": decision,
        }

    # --------------------------------------------------
    # ESCALATION
    # --------------------------------------------------

    if intent == "escalation":

        if not ticket_id:
            return {
                "intent": intent,
                "status": "needs_information",
                "message": (
                    "Please provide the ticket ID "
                    "you want to escalate."
                ),
            }

        ticket_lookup = lookup_ticket(
            ticket_id
        )

        if not ticket_lookup["found"]:
            return {
                "intent": intent,
                "status": "not_found",
                "message": (
                    f"Ticket {ticket_id} was not found."
                ),
            }

        ticket = ticket_lookup["ticket"]

        if (
            account_id is not None
            and ticket["account_id"] != account_id
        ):
            return {
                "intent": intent,
                "status": "access_denied",
                "message": (
                    "You are not authorised to access "
                    "this ticket."
                ),
            }

        decision = analyze_ticket_decision(
            ticket_id=ticket_id,
            assessment_time=assessment_time,
        )

        pending_action = prepare_escalation(
            decision
        )

        return {
            "intent": intent,
            "status": "action_pending",
            "ticket_id": ticket_id,
            "decision": decision,
            "action": pending_action,
        }

    # --------------------------------------------------
    # DOCUMENT SEARCH
    # --------------------------------------------------

    results = search_parcelpilot_documents(
        query=query,
        account_id=account_id,
        top_k=5,
    )

    return {
        "intent": "document_search",
        "status": "success",
        "results": results,
    }