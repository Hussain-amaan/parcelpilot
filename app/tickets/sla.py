from app.retrieval.search import search_documents
from app.policy.resolver import resolve_for_account


def get_response_target(account_id, severity):
    """
    Determine the applicable first-response target.

    Customer-specific agreements take precedence over
    the current default support policy.
    """

    query = (
        f"{severity} first response target "
        f"support response time"
    )

    results = search_documents(
        query,
        top_k=8
    )

    resolved = resolve_for_account(
        results,
        account_id=account_id,
        query=query
    )

    if not resolved:
        return None

    # The actual response target is contained in the
    # retrieved policy text. Return the evidence for now.
    return resolved