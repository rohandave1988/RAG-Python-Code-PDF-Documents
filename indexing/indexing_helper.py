"""
Helper utilities for indexing operations.
"""

import os
from typing import List, Dict, Any
from pathlib import Path
from loguru import logger

class IndexingHelper:
    """
    Helper class containing utility methods for indexing operations.
    """
    
    @staticmethod
    def validate_pdf_path(pdf_path: str) -> bool:
        """
        Validate if the PDF path exists and is a valid PDF file.
        
        Args:
            pdf_path (str): Path to PDF file
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not pdf_path or not os.path.exists(pdf_path):
            return False
        return pdf_path.lower().endswith('.pdf')
    
    @staticmethod
    def get_file_metadata(file_path: str) -> Dict[str, Any]:
        """
        Extract metadata from file path.
        
        Args:
            file_path (str): Path to file
            
        Returns:
            Dict[str, Any]: File metadata
        """
        path = Path(file_path)
        return {
            'filename': path.name,
            'source': str(path.absolute()),
            'file_size': path.stat().st_size if path.exists() else 0,
            'extension': path.suffix.lower()
        }
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and normalize text content.
        
        Args:
            text (str): Raw text
            
        Returns:
            str: Cleaned text
        """
        if not text:
            return ""
            
        # Normalize line endings
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # Remove excessive whitespace
        while '\n\n\n' in text:
            text = text.replace('\n\n\n', '\n\n')
        
        # Normalize spaces
        text = ' '.join(text.split())
        
        return text.strip()
    
    @staticmethod
    def validate_chunk_data(chunks: List[Dict], embeddings: Any) -> bool:
        """
        Validate chunk data and embeddings match.
        
        Args:
            chunks (List[Dict]): List of text chunks
            embeddings: Embedding vectors
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not chunks or embeddings is None:
            return False
            
        try:
            if hasattr(embeddings, '__len__'):
                return len(chunks) == len(embeddings)
            return False
        except:
            return False
    
    @staticmethod
    def find_pdf_files(directory: str) -> List[str]:
        """
        Find all PDF files in a directory.
        
        Args:
            directory (str): Directory path
            
        Returns:
            List[str]: List of PDF file paths
        """
        if not os.path.exists(directory):
            logger.warning(f"Directory does not exist: {directory}")
            return []
        
        pdf_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_files.append(os.path.join(root, file))
        
        return pdf_files
    
    @staticmethod
    def create_batch_metadata(chunks: List[Dict], source_info: Dict) -> List[Dict]:
        """
        Create metadata for a batch of chunks.
        
        Args:
            chunks (List[Dict]): List of chunks
            source_info (Dict): Source document information
            
        Returns:
            List[Dict]: Enhanced chunks with metadata
        """
        enhanced_chunks = []
        
        for i, chunk in enumerate(chunks):
            metadata = chunk.get('metadata', {})
            metadata.update({
                'batch_id': source_info.get('batch_id', ''),
                'processing_timestamp': source_info.get('timestamp', ''),
                'chunk_index': i,
                'total_chunks_in_batch': len(chunks)
            })
            
            enhanced_chunk = chunk.copy()
            enhanced_chunk['metadata'] = metadata
            enhanced_chunks.append(enhanced_chunk)
        
        return enhanced_chunks
    
    @staticmethod
    def calculate_processing_stats(results: List[Dict]) -> Dict:
        """
        Calculate statistics from processing results.
        
        Args:
            results (List[Dict]): List of processing results
            
        Returns:
            Dict: Processing statistics
        """
        if not results:
            return {
                'total_files': 0,
                'successful': 0,
                'failed': 0,
                'total_chunks': 0,
                'success_rate': 0.0
            }
        
        successful = sum(1 for r in results if r.get('success', False))
        total_chunks = sum(r.get('chunks_created', 0) for r in results if r.get('success', False))
        
        return {
            'total_files': len(results),
            'successful': successful,
            'failed': len(results) - successful,
            'total_chunks': total_chunks,
            'success_rate': round(successful / len(results) * 100, 2) if results else 0.0
        }