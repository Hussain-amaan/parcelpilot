from app.tickets.decision import analyze_ticket_decision
from app.agent.validator import validate_response


decision = analyze_ticket_decision(
    ticket_id="TKT-501",
    assessment_time="16-08-2026 10:50"
)


print("=" * 80)
print("VALID RESPONSE TEST")
print("=" * 80)


valid_response = """
Hello Northstar Logistics,

Your issue has been classified as P1.

The applicable P1 response target is 15 minutes.
The SLA has been breached and escalation is required.

Best regards,
ParcelPilot Customer Support
"""


result = validate_response(
    valid_response,
    decision
)

print(result)


print("\n" + "=" * 80)
print("INVALID RESPONSE TEST")
print("=" * 80)


invalid_response = """
Hello Northstar Logistics,

Your issue has been classified as P2.

The applicable response target is 2 hours.
The SLA has not been breached.

Best regards,
ParcelPilot Customer Support
"""


result = validate_response(
    invalid_response,
    decision
)

print(result)