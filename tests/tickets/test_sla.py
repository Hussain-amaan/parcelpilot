from app.tickets.sla import get_response_target


tests = [
    ("ACCT-001", "P1"),
    ("ACCT-001", "P2"),
    ("ACCT-001", "P3"),
    ("ACCT-002", "P1"),
    ("ACCT-002", "P2"),
    ("ACCT-002", "P3"),
    ("ACCT-003", "P1"),
    ("ACCT-004", "P1"),
]


for account_id, severity in tests:

    print("\n")
    print("=" * 80)
    print(
        f"ACCOUNT: {account_id} | "
        f"SEVERITY: {severity}"
    )
    print("=" * 80)

    results = get_response_target(
        account_id,
        severity
    )

    if not results:
        print("No SLA evidence found.")
        continue

    for result in results[:2]:

        metadata = result["metadata"]

        print("\nSource:")
        print(metadata["source"])

        print("Status:")
        print(metadata["status"])

        print("Account:")
        print(metadata.get("account_id"))

        print("\nEvidence:")
        print(result["text"])