from app.agent.chat_router import handle_chat_query


def run(query, account_id=None):

    print("=" * 80)
    print("USER:")
    print(query)

    result = handle_chat_query(
        query=query,
        account_id=account_id,
    )

    print("\nRESULT:")
    print(result)


if __name__ == "__main__":

    run(
        "Can Northstar cancel ORD-1001 without a cancellation fee?",
        account_id="ACCT-001",
    )

    run(
        "A pickup is 3 hours late because of carrier fault. "
        "Should I get a service credit for ORD-2001?",
        account_id="ACCT-002",
    )

    run(
        "What is the SLA for TKT-501?",
        account_id="ACCT-001",
    )

    run(
        "Escalate TKT-501",
        account_id="ACCT-001",
    )