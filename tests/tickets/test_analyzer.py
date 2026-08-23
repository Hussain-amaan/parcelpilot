from app.tickets.analyzer import analyze_ticket


ticket_ids = [
    "TKT-501",
    "TKT-502",
    "TKT-503",
    "TKT-504",
    "TKT-505",
]


for ticket_id in ticket_ids:

    result = analyze_ticket(ticket_id)

    ticket = result["ticket"]
    account = result["account"]

    print("\n")
    print("=" * 80)
    print(f"TICKET: {ticket_id}")
    print("=" * 80)

    print("Account:", account["account_name"])
    print("Plan:", account["plan"])
    print("Subject:", ticket["subject"])
    print("Severity:", result["severity"])

    print("\nDescription:")
    print(ticket["description"])

    print("\nOrders:")
    for order in result["orders"]:
        print(
            order["order_id"],
            "|",
            order["carrier"],
            "|",
            order["status"]
        )