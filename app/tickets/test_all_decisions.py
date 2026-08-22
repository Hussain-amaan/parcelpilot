from app.tickets.decision import analyze_ticket_decision


tickets = [
    ("TKT-501", "16-08-2026 10:50"),
    ("TKT-502", "16-08-2026 10:50"),
    ("TKT-503", "16-08-2026 10:50"),
    ("TKT-504", "16-08-2026 11:00"),
    ("TKT-505", "16-08-2026 10:50"),
]


for ticket_id, assessment_time in tickets:

    result = analyze_ticket_decision(
        ticket_id,
        assessment_time
    )

    print("=" * 80)
    print("TICKET:", result["ticket_id"])
    print("ACCOUNT:", result["account"])
    print("PLAN:", result["plan"])
    print("SEVERITY:", result["severity"])

    print("\nSLA:")
    print(result["sla"])

    print("\nSLA RESULT:")
    print(result["sla_result"])

    print("\nESCALATION:")
    print(result["escalation_required"])

    print("\nKNOWN ISSUES:")

    for issue in result["known_issues"]:
        print("-", issue["issue_id"])

    print("\nRECOMMENDATIONS:")

    for recommendation in result["recommendations"]:
        print("-", recommendation["issue_id"])
        print(" ", recommendation["action"])

    print("\nSERVICE CREDIT:")

    print(result["service_credit"])