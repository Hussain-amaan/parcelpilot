from app.tickets.decision import analyze_ticket_decision
from app.agent.response_generator import generate_response


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

    response = generate_response(result)

    print("=" * 80)
    print(f"TICKET: {ticket_id}")
    print("=" * 80)
    print(response)
    print("\nResponse Source:")
    print(result["response_source"])
    print()