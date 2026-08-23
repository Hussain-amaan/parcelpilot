from app.retrieval.search import search_documents


def search_parcelpilot_documents(
    query: str,
    account_id: str | None = None,
    top_k: int = 5,
):
    """
    Search ParcelPilot's supplied document knowledge base.

    This tool is read-only.
    """

    results = search_documents(
        query=query,
        top_k=top_k,
        account_id=account_id,
    )

    return results