from app.data.queries import (
    get_account,
    get_order,
    get_ticket,
    get_orders_for_account,
    get_tickets_for_account
)


print("\nACCOUNT")
print(get_account("ACCT-001"))


print("\nORDER")
print(get_order("ORD-1001"))


print("\nTICKET")
print(get_ticket("TKT-501"))


print("\nNORTHSTAR ORDERS")
print(get_orders_for_account("ACCT-001"))


print("\nNORTHSTAR TICKETS")
print(get_tickets_for_account("ACCT-001"))