"""
RAG system.
"""

import os
from indexing import PDFProcessor, TextChunker, TextEmbedder, VectorDatabase
from searching import RAGSearcher

class RAGSystem:
    """RAG system."""
    
    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.text_chunker = TextChunker()
        self.embedder = TextEmbedder()
        self.vector_db = VectorDatabase()
        self.searcher = RAGSearcher(self.vector_db, self.embedder)
    
    def index_pdf(self, pdf_path: str):
        """Index a PDF file."""
        text = self.pdf_processor.extract_text(pdf_path)
        chunks = self.text_chunker.create_chunks(text, pdf_path)
        embeddings = self.embedder.embed_batch([chunk["content"] for chunk in chunks])
        return self.vector_db.store_embeddings(chunks, embeddings)
    
    def search(self, query: str) -> dict:
        """Search and get answer."""
        return self.searcher.search(query)

if __name__ == "__main__":
    rag = RAGSystem()
    
    # Example usage
    # rag.index_pdf("document.pdf")
    # result = rag.search("What is machine learning?")
    # print(result["answer"])