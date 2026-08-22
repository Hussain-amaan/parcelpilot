def evaluate_cancellation(
    order,
    account,
    minutes_since_booking
):
    """
    Evaluate whether an order can be cancelled
    and determine the applicable cancellation fee.
    """

    status = order["status"]
    account_id = account["account_id"]

    # Northstar custom cancellation rule
    if account_id == "ACCT-001":
        if status == "BOOKED":
            return {
                "can_cancel": True,
                "fee_inr": 0,
                "reason": (
                    "Northstar may cancel any BOOKED shipment "
                    "before pickup with no cancellation fee."
                )
            }

    # Standard rules
    if status == "DRAFT":
        return {
            "can_cancel": True,
            "fee_inr": 0,
            "reason": "DRAFT shipments may be cancelled with no fee."
        }

    if status == "BOOKED":
        if minutes_since_booking <= 30:
            return {
                "can_cancel": True,
                "fee_inr": 0,
                "reason": "BOOKED shipment is within the 30-minute no-fee window."
            }

        return {
            "can_cancel": True,
            "fee_inr": 250,
            "reason": "BOOKED shipment is beyond the 30-minute no-fee window."
        }

    if status == "PICKED_UP":
        return {
            "can_cancel": False,
            "fee_inr": None,
            "reason": (
                "PICKED_UP shipments cannot be cancelled. "
                "Use the return-to-origin workflow."
            )
        }

    if status == "DELIVERED":
        return {
            "can_cancel": False,
            "fee_inr": None,
            "reason": "DELIVERED shipments cannot be cancelled."
        }

    return {
        "can_cancel": False,
        "fee_inr": None,
        "reason": f"Unknown shipment status: {status}"
    }