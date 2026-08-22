from typing import List, Dict


SOURCE_PRIORITY = {
    "customer_agreement": 1,
    "support_policy": 2,
    "cancellation_service_credit_sop": 2,
    "product_operations": 3,
}


def rank_evidence(results: List[Dict]) -> List[Dict]:
    """
    Rank retrieved evidence using ParcelPilot's
    documented source precedence.

    Customer agreement > current support policy /
    current SOP > product documentation.

    Deprecated documents should not override current sources.
    """

    def score(result):

        metadata = result["metadata"]

        priority = metadata.get("priority", 99)

        status = metadata.get("status", "")

        # Deprecated sources should be lower priority
        if status == "DEPRECATED":
            priority = 99

        return (
            priority,
            result["distance"]
        )

    return sorted(results, key=score)


def resolve_for_account(results, account_id=None):
    """
    Resolve retrieved evidence using account-aware source precedence.

    Rules:
    1. An active customer agreement takes precedence when it is
       relevant to the question.
    2. Otherwise, use current general policy/SOP/product documentation.
    3. Deprecated material must not override current material.
    """

    if not results:
        return []

    # Remove deprecated material from authoritative consideration.
    authoritative = [
        result
        for result in results
        if result["metadata"].get("status") != "DEPRECATED"
    ]

    if not authoritative:
        return []

    account_results = []
    general_results = []

    for result in authoritative:

        metadata = result["metadata"]

        if (
            account_id
            and metadata.get("account_id") == account_id
            and metadata.get("document_type") == "customer_agreement"
            and metadata.get("status") == "ACTIVE"
        ):
            account_results.append(result)

        else:
            general_results.append(result)

    # Best account-specific result
    best_account = None

    if account_results:
        best_account = min(
            account_results,
            key=lambda x: x["distance"]
        )

    # Best general result
    best_general = None

    if general_results:
        best_general = min(
            general_results,
            key=lambda x: (
                x["metadata"].get("priority", 99),
                x["distance"]
            )
        )

    # If account-specific evidence is substantially relevant,
    # prefer it.
    #
    # We use the retrieval distance as an indication of relevance.
    # A lower distance means greater semantic similarity.
    if best_account:

        if best_general is None:
            return [best_account]

        if best_account["distance"] <= best_general["distance"] + 0.25:
            return [best_account]

    # Otherwise use the general authoritative evidence.
    if best_general:
        return [best_general]

    if best_account:
        return [best_account]

    return []


def is_relevant(result, query):
    """
    Basic relevance guard for policy resolution.

    This does not make a business decision.
    It prevents an unrelated account-agreement chunk
    from overriding a relevant general policy.
    """

    query_words = set(
        query.lower().split()
    )

    text = result["text"].lower()

    relevant_terms = [
        word
        for word in query_words
        if len(word) > 3 and word in text
    ]

    return len(relevant_terms) >= 1


def resolve_for_account(results, account_id=None, query=""):

    relevant_results = [
        result
        for result in results
        if is_relevant(result, query)
    ]

    if not relevant_results:
        relevant_results = results

    account_results = [
        result
        for result in relevant_results
        if (
            account_id
            and result["metadata"].get("account_id") == account_id
            and result["metadata"].get("document_type")
            == "customer_agreement"
            and result["metadata"].get("status") == "ACTIVE"
        )
    ]

    if account_results:
        return sorted(
            account_results,
            key=lambda x: x["distance"]
        )

    current_results = [
        result
        for result in relevant_results
        if result["metadata"].get("status") == "CURRENT"
    ]

    if current_results:
        return sorted(
            current_results,
            key=lambda x: (
                x["metadata"].get("priority", 99),
                x["distance"]
            )
        )

    return sorted(
        relevant_results,
        key=lambda x: x["distance"]
    )