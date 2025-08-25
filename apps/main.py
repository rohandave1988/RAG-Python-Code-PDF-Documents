#!/usr/bin/env python3
"""
Main entry point for the Enhanced RAG System.

This script provides multiple ways to interact with the RAG system:
- Interactive demo mode
- Command-line interface  
- Batch processing mode
"""

import sys
import argparse
from pathlib import Path
from loguru import logger

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

# Configure logging
logger.remove()  # Remove default handler
logger.add(
    sys.stdout,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)

from apps.rag_demo import RAGSystem

def run_interactive_demo():
    """Run the interactive demo."""
    from apps.rag_demo import run_enhanced_demo
    run_enhanced_demo()

def run_batch_index(directory: str):
    """Run batch indexing for a directory."""
    print(f"Starting batch indexing for directory: {directory}")
    
    if not Path(directory).exists():
        print(f"Error: Directory '{directory}' does not exist.")
        return False
    
    # Initialize RAG system
    rag = RAGSystem()
    
    # Index directory
    result = rag.index_directory(directory)
    
    if result["success"]:
        stats = result["stats"]
        print(f"✓ Batch indexing completed successfully!")
        print(f"  - Total files: {stats['total_files']}")
        print(f"  - Successful: {stats['successful']}")
        print(f"  - Failed: {stats['failed']}")
        print(f"  - Total chunks created: {stats['total_chunks']}")
        print(f"  - Success rate: {stats['success_rate']}%")
        return True
    else:
        print(f"✗ Batch indexing failed: {result['message']}")
        return False

def run_single_query(query: str, top_k: int = 5):
    """Run a single query and return results."""
    print(f"Processing query: '{query}'")
    
    # Initialize RAG system
    rag = RAGSystem()
    
    # Check system status
    system_info = rag.get_system_info()
    if system_info["system_status"] != "operational":
        print("Error: System is not operational. Please check your setup.")
        return False
    
    # Check if database has content
    db_stats = system_info["indexing"]["database_stats"]
    if db_stats["total_chunks"] == 0:
        print("Error: No documents indexed. Please index some documents first.")
        return False
    
    # Execute query
    result = rag.search(query, top_k=top_k)
    
    if result["success"]:
        print(f"\n💬 Answer:")
        print(f"{result['answer']}")
        
        print(f"\n📚 Sources:")
        for i, source in enumerate(result["sources"], 1):
            similarity_pct = round(source["similarity"] * 100, 1)
            print(f"  {i}. {source['source']} (relevance: {similarity_pct}%)")
        
        metadata = result["search_metadata"]
        print(f"\n⏱️  Processing time: {metadata['total_processing_time']}s")
        return True
    else:
        print(f"✗ Query failed: {result['message']}")
        return False

def show_system_status():
    """Show current system status."""
    print("Checking system status...")
    
    try:
        rag = RAGSystem()
        system_info = rag.get_system_info()
        
        print(f"\n📊 System Status: {system_info['system_status']}")
        
        # Indexing component status
        indexing = system_info["indexing"]
        db_stats = indexing["database_stats"]
        
        print(f"\n📁 Document Database:")
        print(f"  - Total chunks: {db_stats['total_chunks']}")
        print(f"  - Unique sources: {db_stats['unique_sources']}")
        print(f"  - Collection: {db_stats['collection_name']}")
        print(f"  - Database path: {db_stats['database_path']}")
        
        # Embedding model info
        embedding_info = indexing["embedding_model"]
        print(f"\n🧠 Embedding Model:")
        print(f"  - Model: {embedding_info['model_name']}")
        print(f"  - Dimension: {embedding_info['embedding_dimension']}")
        
        # Searching component status
        searching = system_info["searching"]
        components = searching["components"]
        
        print(f"\n🔍 Search Components:")
        print(f"  - Vector Database: {components['vector_database']['status']}")
        print(f"  - Embedding Model: {components['embedding_model']['status']}")
        print(f"  - LLM Model: {components['llm_model']['status']} ({components['llm_model']['model_name']})")
        
        return True
        
    except Exception as e:
        print(f"Error checking system status: {e}")
        return False

def main():
    """Main entry point with command-line argument parsing."""
    parser = argparse.ArgumentParser(
        description="Enhanced RAG System - Document Indexing and Intelligent Search",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Run interactive demo
  %(prog)s --demo                    # Run interactive demo
  %(prog)s --status                  # Show system status
  %(prog)s --index ./documents       # Index all PDFs in directory
  %(prog)s --query "What is AI?"     # Run single query
  %(prog)s --query "How does ML work?" --top-k 3  # Query with custom top-k
        """
    )
    
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Run interactive demo mode (default if no other options)'
    )
    
    parser.add_argument(
        '--status',
        action='store_true',
        help='Show system status and exit'
    )
    
    parser.add_argument(
        '--index',
        metavar='DIRECTORY',
        help='Index all PDF files in the specified directory'
    )
    
    parser.add_argument(
        '--query',
        metavar='QUESTION',
        help='Run a single query and show results'
    )
    
    parser.add_argument(
        '--top-k',
        type=int,
        default=5,
        metavar='N',
        help='Number of top results to retrieve (default: 5)'
    )
    
    args = parser.parse_args()
    
    # If no arguments provided, run interactive demo
    if len(sys.argv) == 1:
        args.demo = True
    
    try:
        # Handle different modes
        if args.status:
            success = show_system_status()
            sys.exit(0 if success else 1)
        
        elif args.index:
            success = run_batch_index(args.index)
            sys.exit(0 if success else 1)
        
        elif args.query:
            success = run_single_query(args.query, args.top_k)
            sys.exit(0 if success else 1)
        
        elif args.demo:
            run_interactive_demo()
            sys.exit(0)
        
        else:
            parser.print_help()
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()