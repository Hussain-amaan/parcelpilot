from app.tools.action_tools import create_escalation


def prepare_escalation(
    decision,
):
    """
    Prepare an escalation without changing system state.

    This function does NOT create the escalation.
    It only returns the information that should be
    shown to the user for confirmation.
    """

    if not decision["escalation_required"]:
        return {
            "action_required": False,
            "message": (
                "This ticket does not currently require escalation."
            ),
        }

    ticket_id = decision["ticket_id"]
    account = decision["account"]
    severity = decision["severity"]

    sla_result = decision["sla_result"]

    reason = (
        f"{severity} incident"
    )

    if sla_result["breached"]:
        reason += " with an SLA breach"

    return {
        "action_required": True,
        "action": "create_escalation",
        "ticket_id": ticket_id,
        "account": account,
        "priority": severity,
        "reason": reason,
        "confirmation_required": True,
        "message": (
            f"Ticket {ticket_id} requires escalation. "
            f"Reason: {reason}. "
            f"Do you want me to create the escalation?"
        ),
    }


def confirm_escalation(
    decision,
    confirmed: bool,
):
    """
    Execute the escalation only after explicit
    user confirmation.
    """

    if not confirmed:
        return {
            "executed": False,
            "message": "Escalation was not created.",
        }

    if not decision["escalation_required"]:
        return {
            "executed": False,
            "message": (
                "Escalation was not created because "
                "the ticket does not require escalation."
            ),
        }

    ticket_id = decision["ticket_id"]

    # We need the account_id for the state-changing tool.
    # It should come from the decision if available.
    account_id = decision.get("account_id")

    if not account_id:
        raise ValueError(
            "account_id is required to create an escalation."
        )

    escalation = create_escalation(
        ticket_id=ticket_id,
        account_id=account_id,
        reason=(
            f"{decision['severity']} incident"
            + (
                " with SLA breach"
                if decision["sla_result"]["breached"]
                else ""
            )
        ),
        priority=decision["severity"],
    )

    return {
        "executed": True,
        "message": (
            f"Escalation {escalation['escalation_id']} "
            f"was created successfully."
        ),
        "escalation": escalation,
    }
