from app.data.queries import (
    get_ticket,
    get_account,
    get_orders_for_account,
)


def classify_severity(ticket):
    """
    Classify ticket severity according to the
    current ParcelPilot Support Policy v3.
    """

    subject = (ticket.get("subject") or "").lower()
    description = (ticket.get("description") or "").lower()

    text = f"{subject} {description}"

    # P1: complete shipment creation outage
    if (
        "all shipment creation" in text
        or (
            "every user" in text
            and "shipment" in text
            and (
                "500" in text
                or "failing" in text
            )
        )
    ):
        return "P1"

    # P1: confirmed/suspected credential exposure
    if (
        "api key exposure" in text
        or "api key" in text
        or "credential exposure" in text
        or "production api key" in text
    ):
        return "P1"

    # P2: major feature degradation
    if (
        "bulk upload" in text
        and (
            "fails" in text
            or "failure" in text
        )
    ):
        return "P2"

    # Default
    return "P3"


def analyze_ticket(ticket_id):
    """
    Retrieve a ticket and its account context,
    then classify the ticket.
    """

    ticket = get_ticket(ticket_id)

    if ticket is None:
        raise ValueError(
            f"Ticket not found: {ticket_id}"
        )

    account_id = ticket["account_id"]

    account = get_account(account_id)

    if account is None:
        raise ValueError(
            f"Account not found: {account_id}"
        )

    orders = get_orders_for_account(account_id)

    severity = classify_severity(ticket)

    return {
        "ticket": ticket,
        "account": account,
        "orders": orders,
        "severity": severity,
    }