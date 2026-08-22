from app.tickets.recommendation import generate_recommendation


ticket = {
    "ticket_id": "TKT-504",
    "subject": "SwiftShip order still shows BOOKED after driver pickup",
    "description": (
        "Driver collected the parcel around 10 minutes ago, "
        "but ParcelPilot still shows BOOKED."
    )
}


known_issues = [
    {
        "issue_id": "KI-211",
        "text": "KI-211 - SwiftShip pickup webhook delay",
        "metadata": {
            "source": "04_Product_Operations_Guide_and_Known_Issues.pdf"
        }
    }
]


recommendations = generate_recommendation(
    ticket,
    known_issues
)


print("=" * 80)
print("RECOMMENDATION TEST")
print("=" * 80)

for recommendation in recommendations:
    print("Issue:", recommendation["issue_id"])
    print("Action:", recommendation["action"])