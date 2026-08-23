from app.tickets.decision import analyze_ticket_decision
from app.agent.llm_response import generate_llm_response


result = analyze_ticket_decision(
    "TKT-502",
    "16-08-2026 10:50"
)

response = generate_llm_response(result)

print("=" * 80)
print("LLM SUPPORT RESPONSE")
print("=" * 80)
print(response)