from app.data.queries import (
    get_ticket,
    get_account,
    get_orders_for_account,
)
from app.tickets.service_credit import evaluate_failed_pickup_credit
from app.tickets.analyzer import classify_severity
from app.tickets.sla import get_response_target
from app.tickets.sla_calculator import calculate_deadline
from app.tickets.sla_parser import parse_response_target, parse_policy_table
from app.tickets.known_issues import find_known_issues
from app.tickets.recommendation import generate_recommendation


def get_sla_target(account, severity):
    """
    Resolve the SLA target for an account and severity.
    """

    account_id = account["account_id"]
    plan = account["plan"]

    results = get_response_target(
        account_id,
        severity
    )

    if not results:
        raise ValueError(
            f"No SLA evidence found for {account_id}"
        )

    # First try customer agreement format.
    for result in results:

        text = result["text"]

        parsed = parse_response_target(
            text,
            severity
        )

        if parsed:
            parsed["source"] = result["metadata"]["source"]
            return parsed

    # Fall back to current policy table.
    for result in results:

        metadata = result["metadata"]

        if (
            metadata.get("document_type")
            == "support_policy"
            and metadata.get("status")
            == "CURRENT"
        ):

            parsed = parse_policy_table(
                result["text"],
                plan,
                severity
            )

            if parsed:
                parsed["source"] = metadata["source"]
                return parsed

    raise ValueError(
        f"Could not parse SLA for "
        f"{account_id}, {severity}"
    )


def analyze_ticket_decision(
    ticket_id,
    assessment_time
):
    """
    Produce a complete support decision
    for a ticket.
    """

    ticket = get_ticket(ticket_id)

    if ticket is None:
        raise ValueError(
            f"Ticket not found: {ticket_id}"
        )

    account = get_account(
        ticket["account_id"]
    )

    if account is None:
        raise ValueError(
            f"Account not found: "
            f"{ticket['account_id']}"
        )

    known_issues = find_known_issues(
    f"{ticket['subject']} {ticket['description']}",
    account_id=account["account_id"]
    )

    recommendations = generate_recommendation(
    ticket,
    known_issues
    )

    orders = get_orders_for_account(
        ticket["account_id"]
    )

    service_credit = None

# Service credits are only evaluated when we have
# enough information to identify a failed pickup.
    pickup_related = (
    "pickup" in ticket["subject"].lower()
    or "pickup" in ticket["description"].lower()
    or "picked up" in ticket["description"].lower()
    )

    if pickup_related:
        service_credit = {
            "eligible": False,
            "credit_inr": 0,
            "reason": (
            "Service-credit assessment requires verified "
            "pickup timing and carrier-fault information."
            )
        }

    severity = classify_severity(ticket)

    sla = get_sla_target(
        account,
        severity
    )

    sla_result = calculate_deadline(
        created_at=ticket["created_at"],
        target_value=sla["target_value"],
        target_unit=sla["target_unit"],
        assessment_time=assessment_time,
    )

    known_issues = find_known_issues(
        f"{ticket['subject']} {ticket['description']}",
        account_id=account["account_id"]
    )

    # P1 incidents must be escalated immediately.
    escalation_required = severity == "P1"

    return {
    "ticket_id": ticket_id,
    "account": account["account_name"],
    "plan": account["plan"],
    "severity": severity,
    "sla": sla,
    "sla_result": sla_result,
    "escalation_required": escalation_required,
    "known_issues": known_issues,
    "recommendations": recommendations,
    "service_credit": service_credit,
    }