# ingest.py
import os
import glob
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_community.document_loaders import CSVLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Paths
PDF_FOLDER = "data/pdfs"
INDEX_PATH = "faiss_index.pkl"


def ingest_data():
    docs = []

    # Load each PDF file individually
    if os.path.exists(PDF_FOLDER):
        pdf_paths = glob.glob(os.path.join(PDF_FOLDER, "*.pdf"))
        for pdf_path in pdf_paths:
            loader = PDFPlumberLoader(pdf_path)
            docs.extend(loader.load())


    # Split into semantic chunks
    splitter = SemanticChunker(HuggingFaceEmbeddings())
    chunks = splitter.split_documents(docs)

    # Embed & index
    embedder = HuggingFaceEmbeddings()
    vector_store = FAISS.from_documents(chunks, embedder)

    # Save index
    vector_store.save_local(INDEX_PATH)
    print(f"Indexed {len(chunks)} chunks to '{INDEX_PATH}'")


if __name__ == '__main__':
    os.makedirs(PDF_FOLDER, exist_ok=True)
    ingest_data()
