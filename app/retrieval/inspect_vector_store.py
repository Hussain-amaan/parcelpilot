from pathlib import Path

import chromadb


BASE_DIR = Path(__file__).resolve().parents[2]
CHROMA_DIR = BASE_DIR / "data" / "chroma"


client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_collection(
    name="parcelpilot_documents"
)

print("Collection:", collection.name)
print("Total chunks:", collection.count())

results = collection.get(
    limit=5
)

print("\nSample records:\n")

for i in range(len(results["ids"])):

    print("=" * 60)
    print("ID:", results["ids"][i])
    print("Metadata:", results["metadatas"][i])
    print("Text:", results["documents"][i][:300])
    