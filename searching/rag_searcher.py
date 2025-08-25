"""
Simple RAG searcher.
"""

from .query_processor import QueryProcessor
from .vector_searcher import VectorSearcher
from .llm_generator import LLMGenerator

class RAGSearcher:
    """Simple RAG searcher."""
    
    def __init__(self, vector_database, embedder, model_name: str = "deepseek-r1:latest"):
        self.query_processor = QueryProcessor()
        self.vector_searcher = VectorSearcher(vector_database, embedder)
        self.llm_generator = LLMGenerator(model_name)
        self.model_name = model_name
    
    def search(self, query: str, top_k: int = 5, response_style: str = "comprehensive") -> dict:
        """Perform complete RAG search."""
        import time
        start_time = time.time()
        
        try:
            # Process query
            query_result = self.query_processor.process_query(query)
            if not query_result["success"]:
                return {"success": False, "message": "Invalid query", "query": query}
            
            # Search documents
            search_result = self.vector_searcher.search(query_result["processed_query"], top_k)
            if not search_result["success"]:
                return {"success": False, "message": "Search failed", "query": query}
            
            # Generate response
            context_docs = [{"content": r["full_content"], "metadata": r["metadata"]} 
                           for r in search_result["results"]]
            
            response = self.llm_generator.generate_rag_response(query, context_docs)
            
            # Format sources for demo compatibility
            formatted_sources = []
            for r in search_result["results"]:
                formatted_sources.append({
                    "source": r["metadata"].get("source", "Unknown"),
                    "similarity": r.get("similarity", 0.0),
                    "content_preview": r["full_content"][:100] + "..." if len(r["full_content"]) > 100 else r["full_content"]
                })
            
            end_time = time.time()
            
            return {
                "success": True,
                "query": query,
                "answer": response.get("response", "No response generated"),
                "sources": formatted_sources,
                "search_metadata": {
                    "total_processing_time": round(end_time - start_time, 2),
                    "documents_retrieved": len(search_result["results"]),
                    "query_processed": query_result["processed_query"]
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "query": query
            }
    
    def get_system_status(self) -> dict:
        """Get system status information."""
        return {
            "components": {
                "llm_model": {
                    "name": self.model_name,
                    "status": "available",
                    "type": "local"
                },
                "query_processor": {
                    "status": "ready"
                },
                "vector_searcher": {
                    "status": "ready"
                }
            },
            "capabilities": {
                "search": True,
                "generation": True,
                "explanation": True
            }
        }
    
    def explain_search_process(self, query: str) -> dict:
        """Explain how a query would be processed."""
        try:
            return {
                "success": True,
                "query": query,
                "explanation": {
                    "query_analysis": {
                        "query_type": "general",
                        "keywords": query.split()[:5]  # First 5 words as keywords
                    },
                    "search_process": {
                        "step1": "Process and clean the user query",
                        "step2": f"Generate embedding for: '{query}'",
                        "step3": "Search vector database for similar documents",
                        "step4": "Retrieve top matching document chunks",
                        "step5": "Generate contextual response using LLM",
                        "step6": "Format and return comprehensive answer"
                    }
                }
            }
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "query": query
            }