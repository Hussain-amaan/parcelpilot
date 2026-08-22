from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parents[2]
CHROMA_DIR = BASE_DIR / "data" / "chroma"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_collection(
    name="parcelpilot_documents"
)

model = SentenceTransformer(EMBEDDING_MODEL)


def search_documents(query, top_k=5):
    """
    Search ParcelPilot documents using semantic similarity.
    """

    query_embedding = model.encode(
        [query]
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    matches = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        matches.append({
            "text": document,
            "metadata": metadata,
            "distance": distance
        })

    return matches