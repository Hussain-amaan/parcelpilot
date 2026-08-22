from pathlib import Path
from pypdf import PdfReader


BASE_DIR = Path(__file__).resolve().parents[2]
DOCUMENTS_DIR = BASE_DIR / "documents"


def load_pdf(file_path):

    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:
        text = page.extract_text(
            extraction_mode="layout"
        )

        if text:
            pages.append(text)

    return "\n".join(pages)


def load_all_pdfs():

    documents = []

    for pdf_file in DOCUMENTS_DIR.glob("*.pdf"):

        text = load_pdf(pdf_file)

        documents.append({
            "filename": pdf_file.name,
            "text": text
        })

    return documents


if __name__ == "__main__":

    documents = load_all_pdfs()

    print(f"Found {len(documents)} PDF files\n")

    for document in documents:

        print("=" * 60)
        print(document["filename"])
        print("=" * 60)

        print(document["text"][:1000])
        print()