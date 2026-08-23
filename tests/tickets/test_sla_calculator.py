from app.tickets.sla_calculator import calculate_deadline


tests = [
    {
        "ticket": "TKT-501",
        "created_at": "16-08-2026 10:30",
        "target_value": 15,
        "target_unit": "minutes",
        "assessment_time": "16-08-2026 10:40",
    },
    {
        "ticket": "TKT-501",
        "created_at": "16-08-2026 10:30",
        "target_value": 15,
        "target_unit": "minutes",
        "assessment_time": "16-08-2026 10:50",
    },
]


for test in tests:

    result = calculate_deadline(
        created_at=test["created_at"],
        target_value=test["target_value"],
        target_unit=test["target_unit"],
        assessment_time=test["assessment_time"],
    )

    print("\n")
    print("=" * 70)
    print("Ticket:", test["ticket"])
    print("Created:", result["created_at"])
    print("Assessment:", result["assessment_time"])
    print("Deadline:", result["deadline"])
    print("Breached:", result["breached"])