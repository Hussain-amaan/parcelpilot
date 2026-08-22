from app.tickets.decision import analyze_ticket_decision


result = analyze_ticket_decision(
    "TKT-504",
    "16-08-2026 11:00"
)

print("=" * 80)
print("TICKET DECISION")
print("=" * 80)

print("Ticket:", result["ticket_id"])
print("Account:", result["account"])
print("Plan:", result["plan"])

print("\nSeverity:")
print(result["severity"])

print("\nSLA:")
print(result["sla"])

print("\nSLA Result:")
print(result["sla_result"])

print("\nEscalation Required:")
print(result["escalation_required"])

print("\nKnown Issues:")

for issue in result["known_issues"]:
    print("Issue:", issue["issue_id"])
    print(issue["text"])

print("\nRecommendations:")

for recommendation in result["recommendations"]:
    print("Issue:", recommendation["issue_id"])
    print("Action:", recommendation["action"])

print("\nRecommendations:")

for recommendation in result["recommendations"]:
    print("Issue:", recommendation["issue_id"])
    print("Action:", recommendation["action"])

print("\nService Credit:")

print(result["service_credit"])    