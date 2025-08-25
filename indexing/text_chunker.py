"""
Simplified text chunking module.
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter

class TextChunker:
    """Simple text chunking."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def create_chunks(self, text: str, source: str = "") -> list:
        """Split text into chunks."""
        chunks = []
        texts = self.splitter.split_text(text)
        for i, chunk_text in enumerate(texts):
            chunks.append({
                "content": chunk_text.strip(),
                "source": source,
                "chunk_id": i
            })
        return chunks
    
    def get_chunker_config(self) -> dict:
        """Get chunker configuration."""
        return {
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "separators": ["\n\n", "\n", " ", ""]
        }
    
    def get_chunk_info(self, chunks: list) -> dict:
        """Get chunk statistics."""
        if not chunks:
            return {"total_chunks": 0, "avg_chunk_size": 0}
        
        total_chars = sum(len(chunk["content"]) for chunk in chunks)
        return {
            "total_chunks": len(chunks),
            "avg_chunk_size": total_chars // len(chunks) if chunks else 0
        }