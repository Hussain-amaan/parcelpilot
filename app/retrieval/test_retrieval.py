from app.retrieval.search import search_documents


queries = [
    "Enterprise P1 response time in the current policy",
    "What was the Enterprise P1 response time in the old policy?",
    "What is the cancellation fee for a BOOKED shipment after 90 minutes?"
]


for query in queries:

    print("\n")
    print("=" * 80)
    print("QUERY:", query)
    print("=" * 80)

    results = search_documents(
        query,
        top_k=3
    )

    for i, result in enumerate(results, start=1):

        print(f"\n--- RESULT {i} ---")

        print("Source:")
        print(result["metadata"]["source"])

        print("\nStatus:")
        print(result["metadata"]["status"])

        print("\nAccount:")
        print(result["metadata"].get("account_id"))

        print("\nDistance:")
        print(result["distance"])

        print("\nText:")
        print(result["text"])