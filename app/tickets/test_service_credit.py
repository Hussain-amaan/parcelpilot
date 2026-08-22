from app.data.queries import get_order, get_account
from app.tickets.service_credit import evaluate_failed_pickup_credit


def test_credit(
    order_id,
    account_id,
    hours_late,
    carrier_fault,
    customer_fault
):
    order = get_order(order_id)
    account = get_account(account_id)

    result = evaluate_failed_pickup_credit(
        order=order,
        account=account,
        hours_late=hours_late,
        carrier_fault=carrier_fault,
        customer_fault=customer_fault
    )

    print("=" * 80)
    print("SERVICE CREDIT TEST")
    print("=" * 80)

    print("Order:", order_id)
    print("Account:", account["account_name"])
    print("Hours late:", hours_late)
    print("Carrier fault:", carrier_fault)
    print("Customer fault:", customer_fault)

    print("\nResult:")
    print(result)


if __name__ == "__main__":

    # LumenWorks:
    # More than 4 hours late → INR 300
    test_credit(
        "ORD-2001",
        "ACCT-002",
        5,
        True,
        False
    )

    # LumenWorks:
    # Only 3 hours late → no credit
    test_credit(
        "ORD-2001",
        "ACCT-002",
        3,
        True,
        False
    )

    # Customer fault → no credit
    test_credit(
        "ORD-2001",
        "ACCT-002",
        6,
        True,
        True
    )

    test_credit(
    "ORD-1001",
    "ACCT-001",
    3,
    True,
    False
    )