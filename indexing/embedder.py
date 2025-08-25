"""
Simplified text embedding module.
"""

import numpy as np
from sentence_transformers import SentenceTransformer

class TextEmbedder:
    """Simple text embedding."""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
    
    def embed_single_text(self, text: str) -> np.ndarray:
        """Embed single text."""
        return self.model.encode(text)
    
    def embed_batch(self, texts: list) -> np.ndarray:
        """Embed multiple texts."""
        return self.model.encode(texts)
    
    def embed_chunks(self, chunks: list) -> np.ndarray:
        """Embed chunks (expects list of dicts with 'content' key)."""
        texts = [chunk["content"] for chunk in chunks]
        return self.model.encode(texts)
    
    def get_model_info(self) -> dict:
        """Get model information."""
        return {
            "model_name": self.model_name,
            "embedding_dimension": 384  # MiniLM-L6-v2 dimension
        }