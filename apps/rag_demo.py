"""
Enhanced RAG system demo using the new package structure.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from loguru import logger

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from indexing import DocumentIndexer
from searching import RAGSearcher
from indexing.vector_store import VectorDatabase
from indexing.embedder import TextEmbedder

class RAGSystem:
    """
    Complete RAG system orchestrating indexing and searching components.
    
    This class provides a high-level interface for the RAG system,
    combining document indexing and intelligent search capabilities.
    """
    
    def __init__(self, 
                 chunk_size: int = 1000,
                 chunk_overlap: int = 200,
                 embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
                 llm_model: str = "deepseek-r1:latest",
                 db_path: str = "./vector_db"):
        """
        Initialize the RAG system.
        
        Args:
            chunk_size (int): Size of text chunks for indexing
            chunk_overlap (int): Overlap between chunks
            embedding_model (str): Embedding model name
            llm_model (str): LLM model name
            db_path (str): Vector database path
        """
        logger.info("Initializing RAG System...")
        
        # Initialize shared components
        self.vector_db = VectorDatabase(db_path=db_path)
        self.embedder = TextEmbedder(model_name=embedding_model)
        
        # Initialize indexing component
        self.indexer = DocumentIndexer(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            embedding_model=embedding_model,
            db_path=db_path
        )
        
        # Initialize searching component
        self.searcher = RAGSearcher(
            self.vector_db,
            self.embedder,
            model_name=llm_model
        )
        
        logger.info("RAG System initialized successfully!")
    
    def index_document(self, pdf_path: str) -> dict:
        """
        Index a single PDF document.
        
        Args:
            pdf_path (str): Path to PDF file
            
        Returns:
            dict: Indexing result
        """
        return self.indexer.index_document(pdf_path)
    
    def index_directory(self, directory_path: str = "./documents") -> dict:
        """
        Index all PDF documents in a directory.
        
        Args:
            directory_path (str): Path to directory containing PDFs
            
        Returns:
            dict: Batch indexing results
        """
        return self.indexer.index_directory(directory_path)
    
    def search(self, query: str, top_k: int = 5, response_style: str = "comprehensive") -> dict:
        """
        Search for information and generate a response.
        
        Args:
            query (str): User question
            top_k (int): Number of documents to retrieve
            response_style (str): Style of response (comprehensive, concise, detailed)
            
        Returns:
            dict: Search results with generated response
        """
        return self.searcher.search(query, top_k=top_k, response_style=response_style)
    
    def get_system_info(self) -> dict:
        """
        Get comprehensive system information.
        
        Returns:
            dict: System status and statistics
        """
        try:
            indexer_status = self.indexer.get_indexer_status()
            searcher_status = self.searcher.get_system_status()
            
            return {
                "system_status": "operational",
                "indexing": indexer_status,
                "searching": searcher_status,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return {
                "system_status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def explain_query(self, query: str) -> dict:
        """
        Explain how a query would be processed.
        
        Args:
            query (str): Query to explain
            
        Returns:
            dict: Process explanation
        """
        return self.searcher.explain_search_process(query)

def run_enhanced_demo():
    """
    Run an enhanced demonstration of the RAG system.
    """
    print("=== Enhanced RAG System Demo ===\n")
    
    # Initialize RAG system
    print("1. Initializing RAG system...")
    try:
        rag = RAGSystem(
            chunk_size=1000,
            chunk_overlap=200,
            embedding_model="sentence-transformers/all-MiniLM-L6-v2",
            llm_model="deepseek-r1:latest"
        )
        print("✓ RAG system initialized successfully\n")
    except Exception as e:
        print(f"✗ Failed to initialize RAG system: {e}")
        print("Make sure all dependencies are installed and Ollama is running.")
        return
    
    # Check system status
    print("2. Checking system status...")
    system_info = rag.get_system_info()
    
    if system_info["system_status"] == "operational":
        print("✓ All components operational")
        
        # Display system info
        db_stats = system_info["indexing"]["database_stats"]
        print(f"  - Database: {db_stats['total_chunks']} chunks from {db_stats['unique_sources']} sources")
        print(f"  - Embedding model: {system_info['indexing']['embedding_model']['model_name']}")
        print(f"  - LLM status: {system_info['searching']['components']['llm_model']['status']}")
        print()
    else:
        print(f"✗ System status: {system_info['system_status']}")
        if "error" in system_info:
            print(f"  Error: {system_info['error']}")
        print()
    
    # Index documents
    documents_folder = "./documents"
    print(f"3. Indexing documents from '{documents_folder}'...")
    
    if not os.path.exists(documents_folder):
        os.makedirs(documents_folder)
        print(f"✓ Created '{documents_folder}' folder")
        print(f"  Please add PDF files to this folder and run the demo again.")
        return
    
    indexing_result = rag.index_directory(documents_folder)
    
    if indexing_result["success"]:
        stats = indexing_result["stats"]
        print(f"✓ Successfully indexed documents:")
        print(f"  - Total files: {stats['total_files']}")
        print(f"  - Successful: {stats['successful']}")
        print(f"  - Total chunks created: {stats['total_chunks']}")
        print(f"  - Success rate: {stats['success_rate']}%")
        
        # Show processed files
        if stats['successful'] > 0:
            print(f"\nProcessed files:")
            for file_result in indexing_result["processed_files"]:
                if file_result["success"]:
                    status = "✓"
                    chunks = file_result.get("chunks_created", 0)
                    print(f"  {status} {file_result['file_path']} ({chunks} chunks)")
                else:
                    print(f"  ✗ {file_result['file_path']} - {file_result['message']}")
        print()
    else:
        print(f"✗ Indexing failed: {indexing_result['message']}")
        return
    
    # Check if we have any indexed documents
    final_system_info = rag.get_system_info()
    total_chunks = final_system_info["indexing"]["database_stats"]["total_chunks"]
    
    if total_chunks == 0:
        print("No documents were successfully indexed. Please check your PDF files and try again.")
        return
    
    print("4. Ready for questions!")
    print("You can now ask questions about your documents. Commands:")
    print("  - Type your question and press Enter")
    print("  - Type 'help' for more options")
    print("  - Type 'status' for system information")
    print("  - Type 'quit' or 'exit' to stop")
    print()
    
    # Interactive question-answering loop
    conversation_history = []
    
    while True:
        try:
            user_input = input("❓ Ask a question: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            if user_input.lower() == 'help':
                print("\nAvailable commands:")
                print("  - Ask any question about your documents")
                print("  - 'status' - Show system status")
                print("  - 'explain <question>' - Explain how a question would be processed")
                print("  - 'quit' or 'exit' - Stop the demo")
                print()
                continue
            
            if user_input.lower() == 'status':
                status = rag.get_system_info()
                db_stats = status["indexing"]["database_stats"]
                print(f"\n📊 System Status:")
                print(f"  - Status: {status['system_status']}")
                print(f"  - Documents indexed: {db_stats['unique_sources']}")
                print(f"  - Total chunks: {db_stats['total_chunks']}")
                print(f"  - Database path: {db_stats['database_path']}")
                print()
                continue
            
            if user_input.lower().startswith('explain '):
                question = user_input[8:].strip()
                if question:
                    explanation = rag.explain_query(question)
                    if explanation["success"]:
                        exp = explanation["explanation"]
                        print(f"\n🔍 Process explanation for: '{question}'")
                        print(f"Query type: {exp['query_analysis']['query_type']}")
                        print(f"Keywords: {', '.join(exp['query_analysis']['keywords'])}")
                        print("\nProcessing steps:")
                        for i, (step, desc) in enumerate(exp['search_process'].items(), 1):
                            print(f"  {i}. {desc}")
                        print()
                    else:
                        print(f"Could not explain query: {explanation['message']}")
                else:
                    print("Please provide a question to explain. Example: explain what is AI?")
                continue
            
            # Process the question
            print(f"\n🔍 Searching for: {user_input}")
            
            result = rag.search(user_input, top_k=5, response_style="comprehensive")
            
            if result["success"]:
                print(f"\n💬 Answer:")
                print(f"{result['answer']}")
                
                # Show sources
                if result["sources"]:
                    print(f"\n📚 Sources ({len(result['sources'])} documents):")
                    for i, source in enumerate(result["sources"], 1):
                        similarity_pct = round(source["similarity"] * 100, 1)
                        print(f"  {i}. {source['source']} (relevance: {similarity_pct}%)")
                        print(f"     Preview: {source['content_preview']}")
                
                # Show follow-up questions
                if result.get("follow_up_questions"):
                    print(f"\n🤔 Related questions you might ask:")
                    for i, follow_up in enumerate(result["follow_up_questions"], 1):
                        print(f"  {i}. {follow_up}")
                
                # Show processing info
                metadata = result["search_metadata"]
                print(f"\n⏱️  Processing time: {metadata['total_processing_time']}s | Documents used: {metadata['documents_retrieved']}")
                
                # Save to conversation history
                conversation_history.append({
                    "query": user_input,
                    "response": result["answer"],
                    "timestamp": datetime.now().isoformat()
                })
                
            else:
                print(f"\n❌ Error: {result['message']}")
                if "error" in result:
                    print(f"Details: {result['error']}")
            
            print()  # Blank line for readability
            
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            logger.error(f"Demo error: {e}")
    
    # Show final statistics
    if conversation_history:
        print(f"\n📈 Session Summary:")
        print(f"  - Questions asked: {len(conversation_history)}")
        print(f"  - Session duration: {datetime.now().strftime('%H:%M:%S')}")
    
    print("\nThank you for trying the Enhanced RAG System! 👋")

if __name__ == "__main__":
    run_enhanced_demo()