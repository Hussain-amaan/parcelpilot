from app.tickets.known_issues import find_known_issues


query = (
    "Growth customer bulk upload "
    "4200 row CSV fails large CSV"
)

results = find_known_issues(query)

print("=" * 80)
print("KNOWN ISSUE SEARCH")
print("=" * 80)

for result in results:

    metadata = result["metadata"]

    print("\nSource:")
    print(metadata["source"])

    print("\nText:")
    print(result["text"])