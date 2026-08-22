from app.tickets.sla_parser import parse_response_target


tests = [
    (
        "P1: 15 minutes, 24x7\n"
        "P2: 1 hour\n"
        "P3: 8 business hours",
        "P1",
    ),
    (
        "P1: 2 business hours\n"
        "P2: 4 business hours\n"
        "P3: 2 business days",
        "P2",
    ),
    (
        "Plan P1 P2 P3\n"
        "Standard 4 business hours "
        "1 business day 2 business days",
        "P1",
    ),
]


for text, severity in tests:

    result = parse_response_target(
        text,
        severity
    )

    print("\n")
    print("=" * 70)
    print("Severity:", severity)
    print("Result:", result)