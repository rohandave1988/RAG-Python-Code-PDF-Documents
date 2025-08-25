import os
from typing import Dict
from datetime import datetime
from loguru import logger
from .pdf_processor import PDFProcessor
from .text_chunker import TextChunker
from .embedder import TextEmbedder
from .vector_store import VectorDatabase
from .indexing_helper import IndexingHelper

class DocumentIndexer:
    
    def __init__(self, 
                 chunk_size: int = 1000,
                 chunk_overlap: int = 200,
                 embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
                 db_path: str = "./vector_db",
                 collection_name: str = "documents"):
        logger.info("Initializing DocumentIndexer...")
        
        self.pdf_processor = PDFProcessor()
        self.text_chunker = TextChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self.embedder = TextEmbedder(model_name=embedding_model)
        self.vector_db = VectorDatabase(db_path=db_path)
        
        self.config = {
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "embedding_model": embedding_model,
            "db_path": db_path,
            "collection_name": collection_name
        }
        
        logger.info("DocumentIndexer initialized successfully!")
    
    def index_document(self, pdf_path: str) -> Dict:
        try:
            logger.info(f"Starting to index document: {pdf_path}")
            
            logger.info("Step 1: Extracting text from PDF...")
            text_result = self.pdf_processor.extract_text_with_metadata(pdf_path)
            
            if not text_result["success"]:
                return {
                    "success": False,
                    "message": f"Failed to extract text: {text_result.get('error', 'Unknown error')}",
                    "file_path": pdf_path
                }
            
            text = text_result["text"]
            file_metadata = text_result["metadata"]
            
            if not text.strip():
                return {
                    "success": False,
                    "message": "No text content found in PDF",
                    "file_path": pdf_path
                }
            
            logger.info("Step 2: Creating text chunks...")
            source_metadata = {
                "source": pdf_path,
                "filename": file_metadata.get("filename", os.path.basename(pdf_path)),
                "indexed_at": datetime.now().isoformat(),
                "file_size": file_metadata.get("file_size", 0),
                "page_count": file_metadata.get("page_count", 0)
            }
            
            chunks = self.text_chunker.create_chunks(text, source_metadata)
            
            if not chunks:
                return {
                    "success": False,
                    "message": "No chunks created from text",
                    "file_path": pdf_path
                }
            
            logger.info("Step 3: Generating embeddings...")
            embeddings = self.embedder.embed_chunks(chunks)
            
            if embeddings.size == 0:
                return {
                    "success": False,
                    "message": "Failed to generate embeddings",
                    "file_path": pdf_path
                }
            
            logger.info("Step 4: Storing in vector database...")
            doc_ids = self.vector_db.store_embeddings(chunks, embeddings)
            
            chunk_info = self.text_chunker.get_chunk_info(chunks)
            
            result = {
                "success": True,
                "message": f"Successfully indexed {pdf_path}",
                "file_path": pdf_path,
                "chunks_created": len(chunks),
                "embeddings_generated": len(embeddings),
                "doc_ids": doc_ids,
                "chunk_info": chunk_info,
                "file_metadata": file_metadata,
                "processing_timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Successfully indexed document: {result}")
            return result
            
        except Exception as e:
            error_msg = f"Error indexing document {pdf_path}: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "message": error_msg,
                "file_path": pdf_path,
                "error": str(e)
            }
    
    def index_directory(self, directory_path: str) -> Dict:
        try:
            pdf_files = IndexingHelper.find_pdf_files(directory_path)
            
            if not pdf_files:
                return {
                    "success": False,
                    "message": f"No PDF files found in {directory_path}",
                    "processed_files": [],
                    "stats": IndexingHelper.calculate_processing_stats([])
                }
            
            logger.info(f"Found {len(pdf_files)} PDF files in {directory_path}")
            
            results = []
            for pdf_file in pdf_files:
                logger.info(f"Processing: {os.path.basename(pdf_file)}")
                result = self.index_document(pdf_file)
                results.append(result)
            
            stats = IndexingHelper.calculate_processing_stats(results)
            
            return {
                "success": True,
                "message": f"Processed {len(pdf_files)} PDF files from {directory_path}",
                "directory_path": directory_path,
                "processed_files": results,
                "stats": stats,
                "processing_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            error_msg = f"Error indexing directory {directory_path}: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "message": error_msg,
                "directory_path": directory_path,
                "error": str(e)
            }
    
    def reindex_document(self, pdf_path: str, remove_old: bool = True) -> Dict:
        if remove_old:
            logger.info(f"Removing old chunks for: {pdf_path}")
            deleted_count = self.vector_db.delete_by_source(pdf_path)
            logger.info(f"Removed {deleted_count} old chunks")
        
        result = self.index_document(pdf_path)
        
        if result["success"] and remove_old:
            result["old_chunks_removed"] = deleted_count
            result["message"] += f" (replaced {deleted_count} old chunks)"
        
        return result
    
    def get_indexer_status(self) -> Dict:
        db_stats = self.vector_db.get_database_stats()
        model_info = self.embedder.get_model_info()
        chunker_config = self.text_chunker.get_chunker_config()
        
        return {
            "config": self.config,
            "database_stats": db_stats,
            "embedding_model": model_info,
            "chunker_config": chunker_config,
            "status": "ready"
        }
    
    def optimize_index(self):
        logger.info("Optimizing index...")
        stats = self.vector_db.optimize_database()
        logger.info("Index optimization completed")
        return stats