"""
Simplified vector database module.
"""

import uuid
import chromadb
import numpy as np

class VectorDatabase:
    """Simple vector storage using ChromaDB."""
    
    def __init__(self, db_path: str = "./vector_db"):
        self.client = chromadb.PersistentClient(path=db_path)
        try:
            self.collection = self.client.get_collection("documents")
        except:
            self.collection = self.client.create_collection("documents")
    
    def store_embeddings(self, chunks: list, embeddings: np.ndarray) -> list:
        """Store chunks and embeddings."""
        ids = [str(uuid.uuid4()) for _ in range(len(chunks))]
        contents = [chunk["content"] for chunk in chunks]
        
        # Flatten metadata for ChromaDB compatibility
        metadatas = []
        for chunk in chunks:
            metadata = {"chunk_id": str(chunk["chunk_id"])}
            
            # Handle different chunk formats
            if isinstance(chunk.get("source"), dict):
                # Complex metadata from DocumentIndexer
                source_data = chunk["source"]
                metadata.update({
                    "source": str(source_data.get("source", "")),
                    "filename": str(source_data.get("filename", "")),
                    "indexed_at": str(source_data.get("indexed_at", "")),
                    "file_size": str(source_data.get("file_size", 0)),
                    "page_count": str(source_data.get("page_count", 0))
                })
            else:
                # Simple metadata from basic RAG
                metadata["source"] = str(chunk.get("source", ""))
            
            metadatas.append(metadata)
        
        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=contents,
            metadatas=metadatas,
            ids=ids
        )
        return ids
    
    def search_similar(self, query_embedding: np.ndarray, top_k: int = 5) -> list:
        """Search for similar documents."""
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k,
            include=['documents', 'metadatas', 'distances']
        )
        
        similar_docs = []
        if results['documents'] and results['documents'][0]:
            for doc, metadata, distance in zip(
                results['documents'][0],
                results['metadatas'][0], 
                results['distances'][0]
            ):
                similar_docs.append({
                    'content': doc,
                    'metadata': metadata,
                    'similarity': 1 - distance
                })
        return similar_docs
    
    def get_database_stats(self) -> dict:
        """Get basic database statistics."""
        count = self.collection.count()
        return {
            "total_chunks": count,
            "unique_sources": count,  # Simplified - assume each chunk is from different source
            "collection_name": "documents",
            "database_path": "./vector_db"
        }
    
    def delete_by_source(self, source: str) -> int:
        """Delete documents by source."""
        # Get all documents with matching source
        results = self.collection.get(where={"source": source})
        if results and results["ids"]:
            self.collection.delete(ids=results["ids"])
            return len(results["ids"])
        return 0
    
    def optimize_database(self) -> dict:
        """Optimize database (simplified - just return stats)."""
        return self.get_database_stats()