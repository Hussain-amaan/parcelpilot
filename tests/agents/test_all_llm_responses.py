from app.agent.Agent import run_support_agent


TEST_CASES = [
    ("TKT-501", "16-08-2026 10:50"),
    ("TKT-502", "16-08-2026 10:50"),
    ("TKT-503", "16-08-2026 10:50"),
    ("TKT-504", "16-08-2026 11:00"),
    ("TKT-505", "16-08-2026 10:50"),
]


for ticket_id, assessment_time in TEST_CASES:

    print("=" * 80)
    print(f"TICKET: {ticket_id}")
    print("=" * 80)

    result = run_support_agent(
        ticket_id=ticket_id,
        assessment_time=assessment_time,
    )

    decision = result["decision"]

    print("Account:", decision["account"])
    print("Plan:", decision["plan"])
    print("Severity:", decision["severity"])

    print("\nSLA:")
    print(decision["sla"])

    print("\nSLA Result:")
    print(decision["sla_result"])

    print("\nEscalation:")
    print(decision["escalation_required"])

    print("\nKnown Issues:")
    for issue in decision.get("known_issues", []):
        print("-", issue.get("issue_id"))

    print("\nRecommendations:")
    for recommendation in decision.get("recommendations", []):
        print("-", recommendation.get("issue_id"))
        print(" ", recommendation.get("action"))

    print("\nService Credit:")
    print(decision.get("service_credit"))

    print("\n" + "-" * 80)
    print("CUSTOMER RESPONSE")
    print("-" * 80)

    print(result["response"])

    print("\nResponse Source:")
    print(result["response_source"])

    print("\nValidation:")

    if result["validation"] is None:
        print("Not applicable - deterministic fallback used.")

    else:
        print(result["validation"])

    print()