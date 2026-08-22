from app.tickets.sla_parser import parse_policy_table


tests = [
    ("Enterprise", "P1"),
    ("Enterprise", "P2"),
    ("Enterprise", "P3"),

    ("Growth", "P1"),
    ("Growth", "P2"),
    ("Growth", "P3"),

    ("Standard", "P1"),
    ("Standard", "P2"),
    ("Standard", "P3"),
]


for plan, severity in tests:

    result = parse_policy_table(
        "",
        plan,
        severity
    )

    print("\n")
    print("=" * 70)
    print(
        f"Plan: {plan} | "
        f"Severity: {severity}"
    )
    print("Result:", result)