from app.data.queries import get_order, get_account
from app.policy.cancellation import evaluate_cancellation


def test_cancellation(
    order_id,
    account_id,
    minutes_since_booking
):
    order = get_order(order_id)
    account = get_account(account_id)

    result = evaluate_cancellation(
        order=order,
        account=account,
        minutes_since_booking=minutes_since_booking
    )

    print("=" * 80)
    print("CANCELLATION TEST")
    print("=" * 80)

    print("Order:", order_id)
    print("Account:", account["account_name"])
    print("Status:", order["status"])
    print("Minutes since booking:", minutes_since_booking)

    print("\nResult:")
    print(result)


if __name__ == "__main__":

    # Northstar: custom agreement
    test_cancellation(
        "ORD-1001",
        "ACCT-001",
        90
    )

    # Northstar PICKED_UP
    test_cancellation(
        "ORD-1002",
        "ACCT-001",
        120
    )

    test_cancellation(
    "ORD-2001",
    "ACCT-002",
    90
    )