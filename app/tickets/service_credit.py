from app.retrieval.search import search_documents


def evaluate_failed_pickup_credit(
    order,
    account,
    hours_late,
    carrier_fault,
    customer_fault
):
    """
    Evaluate failed-pickup service-credit eligibility.

    Customer agreements take precedence over the
    default service-credit SOP.
    """

    if order is None:
        raise ValueError("Order not found")

    if account is None:
        raise ValueError("Account not found")

    # Customer fault means no credit.
    if customer_fault:
        return {
            "eligible": False,
            "credit_inr": 0,
            "reason": (
                "Customer-caused issue prevents "
                "service-credit eligibility."
            )
        }

    # Carrier fault must be confirmed.
    if not carrier_fault:
        return {
            "eligible": False,
            "credit_inr": 0,
            "reason": (
                "Carrier fault has not been confirmed. "
                "Do not promise a service credit."
            )
        }

    account_id = account["account_id"]

    # ---------------------------------------------------------
    # Search customer agreement
    # ---------------------------------------------------------

    results = search_documents(
        "failed pickup service credit threshold credit amount",
        top_k=5,
        account_id=account_id
    )

    agreement_text = ""

    for result in results:
        metadata = result["metadata"]

        if (
            metadata.get("document_type") == "customer_agreement"
            and metadata.get("status") == "ACTIVE"
            and metadata.get("account_id") == account_id
        ):
            agreement_text += result["text"] + "\n"

    # ---------------------------------------------------------
    # LumenWorks agreement override
    # ---------------------------------------------------------

    if (
        "LumenWorks" in agreement_text
        and "fixed INR 300" in agreement_text
    ):

        if hours_late > 4:
            return {
                "eligible": True,
                "credit_inr": 300,
                "reason": (
                    "LumenWorks agreement provides a fixed "
                    "INR 300 credit when pickup is more than "
                    "4 hours past the scheduled pickup window."
                )
            }

        return {
            "eligible": False,
            "credit_inr": 0,
            "reason": (
                "LumenWorks pickup is not more than "
                "4 hours past the scheduled pickup window."
            )
        }

    # ---------------------------------------------------------
    # Default current SOP
    # ---------------------------------------------------------

    if hours_late <= 2:
        return {
            "eligible": False,
            "credit_inr": 0,
            "reason": (
                "Pickup is not more than 2 hours past "
                "the scheduled pickup window."
            )
        }

    credit = min(
        500,
        0.10 * order["shipment_fee_inr"]
    )

    return {
        "eligible": True,
        "credit_inr": credit,
        "reason": (
            "Default current service-credit SOP applies: "
            "pickup is more than 2 hours late, carrier fault "
            "is confirmed, and there is no customer-caused issue."
        )
    }