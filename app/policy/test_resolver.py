from app.retrieval.search import search_documents
from app.policy.resolver import resolve_for_account


tests = [
    (
        "What is the cancellation fee for a BOOKED shipment after 90 minutes?",
        "ACCT-001",
    ),
    (
        "What is Northstar's P1 response target?",
        "ACCT-001",
    ),
    (
        "What is the failed-pickup credit for LumenWorks?",
        "ACCT-002",
    ),
    (
        "What is the Bulk Upload limit?",
        "ACCT-001",
    ),
]


for query, account_id in tests:

    print("\n")
    print("=" * 80)
    print("QUERY:", query)
    print("ACCOUNT:", account_id)
    print("=" * 80)

    results = search_documents(
        query,
        top_k=5
    )

    resolved = resolve_for_account(
        results,
        account_id=account_id,
        query=query
)
    for i, result in enumerate(resolved[:3], start=1):

        metadata = result["metadata"]

        print(f"\n--- RESOLVED RESULT {i} ---")
        print("Source:", metadata["source"])
        print("Document type:", metadata["document_type"])
        print("Status:", metadata["status"])
        print("Account:", metadata.get("account_id"))
        print("Distance:", result["distance"])
        print("Text:")
        print(result["text"])