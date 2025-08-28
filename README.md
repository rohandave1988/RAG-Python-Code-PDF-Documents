# Enhanced RAG System

A comprehensive Retrieval-Augmented Generation (RAG) system built with a clean package architecture. This system allows you to index PDF documents and ask intelligent questions about their content using advanced language models.

## 🏗️ Architecture

The system is organized into two main packages:

### 📦 `indexing` Package
Handles document ingestion and processing:

- **`document_indexer.py`** - High-level orchestration of the indexing pipeline
- **`pdf_processor.py`** - PDF text extraction and preprocessing
- **`text_chunker.py`** - Text segmentation and chunking
- **`embedder.py`** - Text-to-vector embedding generation
- **`vector_store.py`** - Vector database operations using ChromaDB
- **`indexing_helper.py`** - Utility functions for indexing operations

### 🔍 `searching` Package
Handles query processing and response generation:

- **`rag_searcher.py`** - High-level orchestration of the search pipeline
- **`query_processor.py`** - Query preprocessing and analysis
- **`vector_searcher.py`** - Vector similarity search operations
- **`llm_generator.py`** - LLM-based response generation using Ollama
- **`search_helper.py`** - Utility functions for search operations

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed
2. **Ollama** running locally with DeepSeek-R1 model:
   ```bash
   # Install Ollama (visit https://ollama.ai for installation)
   ollama serve
   ollama pull deepseek-r1:latest
   ```

### Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

#### Interactive Demo Mode (Recommended)
```bash
python apps/rag_demo.py
```
or
```bash
python apps/main.py --demo
```

This launches an interactive session where you can:
- Index documents from the `./documents` folder
- Ask questions about the indexed content
- Get detailed explanations of the search process

#### Command Line Interface

**Check system status:**
```bash
python apps/main.py --status
```

**Index documents from a directory:**
```bash
python apps/main.py --index ./path/to/pdf/directory
```

**Ask a single question:**
```bash
python apps/main.py --query "What is artificial intelligence?"
```

**Ask a question with custom number of results:**
```bash
python apps/main.py --query "How does machine learning work?" --top-k 3
```

## 🛠️ Helper Classes

Both packages include comprehensive helper classes with utility functions:

### IndexingHelper
- File validation and metadata extraction
- Text cleaning and normalization
- Batch processing utilities
- Statistics calculation

### SearchHelper
- Query preprocessing and validation
- Result ranking and filtering
- Deduplication and formatting
- Performance metrics calculation

## ⚙️ Configuration

### Embedding Models
The system supports various sentence-transformer models:
- `sentence-transformers/all-MiniLM-L6-v2` (default, lightweight)

### LLM Models
Compatible with any Ollama model:
- `deepseek-r1:latest` (default, reasoning-focused)

### Chunking Parameters
- **chunk_size**: Maximum characters per chunk (default: 1000)
- **chunk_overlap**: Characters to overlap between chunks (default: 200)

  System Architecture:-

  ### 📊 System Overview Flow

```
📄 PDF Documents
    ⬇️
🔍 PDF Processor 
    ⬇️
✂️ Text Chunker
    ⬇️  
🧮 Text Embedder
    ⬇️
🗄️ Vector Database ←─────┐
                         │
❓ User Query            │
    ⬇️                   │
🔄 Query Processor       │
    ⬇️                   │
🎯 Vector Searcher ──────┘
    ⬇️
📚 Similar Documents
    ⬇️
🤖 LLM Generator
    ⬇️
💬 Final Answer
```

### 🔄 Component Interaction Flow

**Step-by-Step Process:**

```
👤 User → "What is total revenue?"
    ↓
🔍 RAGSearcher → process_query()
    ↓
✨ QueryProcessor → cleaned query
    ↓
🎯 VectorSearcher → similarity search
    ↓
🗄️ VectorDatabase → top 5 matches
    ↓
🤖 LLMGenerator → contextual response
    ↓
📊 User ← formatted answer + sources + metadata
```

Data Flow Architecture

```
📥 INPUT DATA          🔄 PROCESSING         💾 STORAGE
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│ 📄 PDF Files│ ────► │🔍 Extraction│ ────► │🗄️ Vector DB │
│ 📝 Text Data│       │✂️ Chunking  │       │📇 Indices   │
│ 📊 Tables   │       │🧮 Embeddings│       │             │
└─────────────┘       └─────────────┘       └──────┬──────┘
                                                   │
                                                   ▼
🔍 SEARCH                                  🤖 GENERATION
┌─────────────┐                          ┌─────────────┐
│❓ User Query│ ────────────────────────► │🤖 LLM       │
│🎯 Similarity│                          │💬 Answer    │
│📋 Context   │                          │             │
└─────────────┘                          └─────────────┘
```
💻 RAG Application
├── 🗄️ ChromaDB (Embedded)
├── 🤖 Ollama (Local LLM)
└── 📁 Local PDF Files


  <img width="684" height="295" alt="Rag_Flow_DeepSeek" src="https://github.com/user-attachments/assets/9bcfcd59-35d6-4ea2-ae67-929690d5888c" />





https://github.com/user-attachments/assets/f97ca50d-a111-4137-8034-acf6d5397e0f

