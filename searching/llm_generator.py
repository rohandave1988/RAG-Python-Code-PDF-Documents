"""
Simplified LLM interface module.
"""

import requests
from typing import Dict, List

class LLMGenerator:
    """Simple LLM response generator."""
    
    def __init__(self, model_name: str = "deepseek-r1:latest"):
        self.base_url = "http://localhost:11434"
        self.model_name = model_name
    
    def generate_rag_response(self, query: str, context_docs: List[Dict]) -> Dict:
        """Generate response using retrieved context."""
        try:
            if not context_docs:
                return {
                    "success": False,
                    "response": "No relevant information found.",
                    "query": query
                }
            
            context = self._prepare_context(context_docs)
            prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"
            
            response = self._generate_response(prompt)
            
            return {
                "success": True,
                "response": response,
                "query": query,
                "sources": [doc['metadata'].get('source', 'Unknown') for doc in context_docs]
            }
            
        except Exception as e:
            # Fallback: return context directly when LLM is unavailable
            return self._generate_fallback_response(query, context_docs, str(e))
    
    def _prepare_context(self, context_docs: List[Dict]) -> str:
        """Prepare context from documents."""
        context_parts = []
        for i, doc in enumerate(context_docs[:3], 1):
            content = doc['content'][:500] + "..." if len(doc['content']) > 500 else doc['content']
            context_parts.append(f"[{i}] {content}")
        return "\n\n".join(context_parts)
    
    def _generate_response(self, prompt: str) -> str:
        """Generate response from LLM."""
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }
        
        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        return response.json().get('response', '')
    
    def _generate_fallback_response(self, query: str, context_docs: List[Dict], error: str) -> Dict:
        """Generate a fallback response when LLM is unavailable."""
        context_text = self._prepare_context(context_docs)
        
        # Create a basic response by extracting relevant information
        response = f"Based on the retrieved documents, here's the relevant information for your question '{query}':\n\n"
        response += f"Retrieved Context:\n{context_text}\n\n"
        response += f"Note: LLM service unavailable ({error.split(':')[0]}), showing raw context. "
        response += "To get enhanced AI-generated responses, please start the Ollama service with: 'ollama serve' and ensure the model is available."
        
        return {
            "success": True,
            "response": response,
            "query": query,
            "sources": [doc['metadata'].get('source', 'Unknown') for doc in context_docs],
            "fallback": True
        }
    
    def check_llm_availability(self) -> bool:
        """Check if LLM service is available."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False