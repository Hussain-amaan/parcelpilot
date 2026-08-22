from app.retrieval.pdf_loader import load_all_pdfs
from app.retrieval.text_processing import clean_text
from app.retrieval.chunker import chunk_text
from app.retrieval.metadata import get_metadata


def process_documents():
    """
    Load, clean, chunk, and attach metadata
    to all PDF documents.
    """

    documents = load_all_pdfs()

    processed_chunks = []

    for document in documents:

        filename = document["filename"]

        # Clean PDF text
        cleaned_text = clean_text(document["text"])

        # Split into logical chunks
        chunks = chunk_text(cleaned_text)

        # Get document metadata
        metadata = get_metadata(filename)

        if metadata is None:
            raise ValueError(
                f"No metadata found for document: {filename}"
            )

        # Attach metadata to every chunk
        for index, chunk in enumerate(chunks):

            chunk_metadata = {
                **metadata,
                "source": filename,
                "chunk_id": index
            }

            processed_chunks.append({
                "text": chunk,
                "metadata": chunk_metadata
            })

    return processed_chunks


if __name__ == "__main__":

    chunks = process_documents()

    print(f"Total chunks: {len(chunks)}\n")

    for i, item in enumerate(chunks, start=1):

        print("=" * 70)
        print(f"CHUNK {i}")
        print("=" * 70)

        print("Metadata:")
        print(item["metadata"])

        print("\nText:")
        print(item["text"][:500])
        print()