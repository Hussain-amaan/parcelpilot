from app.tickets.decision import analyze_ticket_decision
from app.agent.action_manager import (
    prepare_escalation,
    confirm_escalation,
)


decision = analyze_ticket_decision(
    "TKT-501",
    "16-08-2026 10:50",
)

print("=" * 80)
print("ACTION TEST")
print("=" * 80)

print("\nSTEP 1: DECISION")
print(decision)

print("\nSTEP 2: PREPARE ESCALATION")

pending = prepare_escalation(decision)

print(pending)

print("\nSTEP 3: WITHOUT CONFIRMATION")

result = confirm_escalation(
    decision,
    confirmed=False,
)

print(result)

print("\nSTEP 4: WITH CONFIRMATION")

result = confirm_escalation(
    decision,
    confirmed=True,
)

print(result)