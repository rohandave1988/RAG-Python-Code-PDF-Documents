"""
Simple vector search.
"""

class VectorSearcher:
    """Simple vector searcher."""
    
    def __init__(self, vector_database, embedder):
        self.vector_db = vector_database
        self.embedder = embedder
    
    def search(self, query: str, top_k: int = 5) -> dict:
        """Search for similar documents."""
        try:
            query_embedding = self.embedder.embed_single_text(query)
            results = self.vector_db.search_similar(query_embedding, top_k=top_k)
            
            formatted_results = []
            for i, result in enumerate(results):
                formatted_results.append({
                    'rank': i + 1,
                    'content': result['content'][:200] + "..." if len(result['content']) > 200 else result['content'],
                    'full_content': result['content'],
                    'metadata': result['metadata'],
                    'similarity': result.get('similarity', 0)
                })
            
            return {
                "success": True,
                "query": query,
                "results": formatted_results
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "results": [],
                "query": query
            }