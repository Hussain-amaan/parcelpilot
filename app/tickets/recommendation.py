def generate_recommendation(ticket, known_issues):
    """
    Generate an operational recommendation
    based on the ticket and known issues.
    """

    recommendations = []

    for issue in known_issues:

        issue_id = issue["issue_id"]

        if issue_id == "KI-208":
            recommendations.append({
                "issue_id": "KI-208",
                "action": (
                    "Split the CSV into files below 3,000 rows. "
                    "Individual shipment creation remains unaffected."
                )
            })

        elif issue_id == "KI-211":
            recommendations.append({
                "issue_id": "KI-211",
                "action": (
                    "Verify the carrier status or wait through "
                    "the known 20-minute webhook delay window. "
                    "Do not tell the customer that pickup did not occur "
                    "based only on the BOOKED status."
                )
            })

    return recommendations