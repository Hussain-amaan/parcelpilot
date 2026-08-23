from app.data.queries import (
    get_ticket,
    get_account,
    get_orders_for_account,
)

from app.policy.cancellation import evaluate_cancellation
from app.tickets.service_credit import evaluate_failed_pickup_credit
from datetime import datetime

def lookup_ticket(ticket_id: str):
    """
    Look up a support ticket.
    """

    ticket = get_ticket(ticket_id)

    if ticket is None:
        return {
            "found": False,
            "ticket_id": ticket_id,
        }

    return {
        "found": True,
        "ticket": ticket,
    }


def lookup_account(account_id: str):
    """
    Look up an account.
    """

    account = get_account(account_id)

    if account is None:
        return {
            "found": False,
            "account_id": account_id,
        }

    return {
        "found": True,
        "account": account,
    }


def lookup_orders(account_id: str):
    """
    Look up orders belonging to an account.
    """

    orders = get_orders_for_account(account_id)

    return {
        "account_id": account_id,
        "orders": orders,
    }


def check_cancellation(
    order,
    account,
    reference_time,
):
    """
    Evaluate whether an order can be cancelled.

    The elapsed time since booking is calculated from
    the supplied order data and reference time.
    """

    booked_at = datetime.strptime(
        order["booked_at"],
        "%d-%m-%Y %H:%M",
    )

    reference_time = datetime.strptime(
        reference_time,
        "%d-%m-%Y %H:%M",
    )

    minutes_since_booking = (
        reference_time - booked_at
    ).total_seconds() / 60

    result = evaluate_cancellation(
        order=order,
        account=account,
        minutes_since_booking=minutes_since_booking,
    )

    # Include the calculated value for transparency.
    result["minutes_since_booking"] = minutes_since_booking

    return result


def check_service_credit(
    order,
    account,
    hours_late,
    carrier_fault,
    customer_fault,
):
    """
    Evaluate service-credit eligibility.
    """

    return evaluate_failed_pickup_credit(
        order=order,
        account=account,
        hours_late=hours_late,
        carrier_fault=carrier_fault,
        customer_fault=customer_fault,
    )