"""
Simple query processing.
"""

import re

class QueryProcessor:
    """Simple query processor."""
    
    def process_query(self, raw_query: str) -> dict:
        """Process query."""
        cleaned = re.sub(r'[^\w\s]', '', raw_query).strip().lower()
        
        return {
            "success": bool(cleaned),
            "original_query": raw_query,
            "processed_query": cleaned
        }