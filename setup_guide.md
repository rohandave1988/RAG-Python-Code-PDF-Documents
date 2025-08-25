# RAG System Setup and Running Guide

## Overview
This RAG (Retrieval-Augmented Generation) system processes PDF documents from a `documents` folder and answers questions based on their content using DeepSeek-R1 model via Ollama.

## System Architecture

```
Documents Folder → PDF Processing → Chunking → Embeddings → Vector DB → Query Processing → LLM Response
```

### Components:
1. **PDF Processor** - Extracts text from PDF files
2. **Text Chunker** - Splits text into manageable chunks
3. **Text Embedder** - Converts text to vector embeddings
4. **Vector Database** - Stores and searches embeddings
5. **LLM Interface** - Generates responses using DeepSeek-R1

## Prerequisites

### 1. Install Ollama
```bash
# Download and install Ollama from https://ollama.ai
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve
```

### 2. Install DeepSeek-R1 Model
```bash
# Pull the DeepSeek-R1 model
ollama pull deepseek-r1:latest
```

### 3. Python Requirements
- Python 3.8+
- pip package manager

## Installation Steps

### 1. Clone or Download Files
Create a new directory and save all the Python files:
- `pdf_processor.py`
- `chunking.py` 
- `embedding.py`
- `vector_database.py`
- `llm_interface.py`
- `simple_rag_demo.py`
- `setup_and_run.py`
- `config.py`
- `requirements.txt`

### 2. Install Python Dependencies
```bash
# Create virtual environment (recommended)
python -m venv rag_env
source rag_env/bin/activate  # On Windows: rag_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Create Documents Folder and Add PDFs
```bash
# Create documents folder
mkdir documents

# Copy your PDF files to the documents folder
cp /path/to/your/pdfs/*.pdf documents/
```

### 4. Verify Ollama is Running
```bash
# Check if Ollama is accessible
curl http://localhost:11434/api/tags

# Should return JSON with available models including deepseek-r1
```

## Running the System

### Method 1: Complete Setup and Demo Script (Recommended)
```bash
# This will setup folders, check for PDFs, and run interactive demo
python setup_and_run.py
```

This script will:
- Create necessary folders (`documents`, `vector_db`, `logs`)
- Check for PDF files in the documents folder
- Offer quick demo or interactive mode
- Process all PDFs automatically

### Method 2: Simple Demo Script
```bash
# Make sure you have PDF files in ./documents/ folder
python simple_rag_demo.py
```

### Method 3: Manual Usage
```python
from simple_rag_demo import SimpleRAGDemo

# Initialize system
rag = SimpleRAGDemo()

# Process all PDFs from documents folder
result = rag.add_documents_from_folder("./documents")
print(f"Processed {result['successful_files']} files")

# Ask questions
answer = rag.ask_question("What are these documents about?")
print(answer["answer"])
```

## File Structure
```
rag_system/
├── documents/            # 📁 PUT YOUR PDF FILES HERE
│   ├── document1.pdf
│   ├── document2.pdf
│   └── ...
├── pdf_processor.py      # PDF text extraction
├── chunking.py          # Text chunking logic
├── embedding.py         # Text to vector conversion
├── vector_database.py   # Vector storage and search
├── llm_interface.py     # Ollama/DeepSeek-R1 interface
├── simple_rag_demo.py   # Main demo system
├── setup_and_run.py     # Setup and interactive demo
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── vector_db/           # Vector database files (auto-created)
├── uploads/             # Additional uploads (auto-created)
└── logs/                # Log files (auto-created)
```

## Quick Start Guide

1. **Install Ollama and DeepSeek-R1**
2. **Install Python dependencies**: `pip install -r requirements.txt`
3. **Create documents folder**: `mkdir documents`
4. **Add your PDF files to documents folder**
5. **Run**: `python setup_and_run.py`

## Demo Modes

### 1. Quick Demo Mode
- Processes all PDFs in documents folder
- Asks 4 predefined questions
- Shows answers and sources used

### 2. Interactive Demo Mode
- Processes all PDFs in documents folder
- Allows you to ask custom questions
- Type 'quit' to exit
- Shows source documents for each answer

## Example Usage

```bash
$ python setup_and_run.py

🚀 RAG System Setup and Demo
========================================
Setting up folders...
✓ Created/verified folder: ./documents
✓ Created/verified folder: ./vector_db
✓ Created/verified folder: ./logs

📄 Found 3 PDF files in documents folder:
  - research_paper.pdf
  - manual.pdf
  - report.pdf

Select demo mode:
1. Quick demo (predefined questions)
2. Interactive demo (ask your own questions)
3. Exit

Enter your choice (1-3): 2

==================================================
PROCESSING DOCUMENTS
==================================================
✅ Successfully processed 3 documents
📊 Total chunks created: 45

==================================================
INTERACTIVE Q&A SESSION
==================================================
Ask questions about your documents (type 'quit' to exit)

🤔 Your Question: What is the main topic of these documents?

🔍 Searching for relevant information...

🤖 Answer: Based on the documents, the main topics cover artificial intelligence research methodologies, technical system documentation, and performance analysis reports...

📚 Used 3 source(s)

📖 Source excerpts:
1. From research_paper.pdf (similarity: 0.89)
   This paper presents a novel approach to machine learning...
```

## Configuration

### Default Settings (in config.py)
- **Documents Folder**: ./documents
- **Chunk Size**: 1000 characters
- **Chunk Overlap**: 200 characters
- **Embedding Model**: sentence-transformers/all-MiniLM-L6-v2
- **Vector DB Path**: ./vector_db
- **Max Retrieved Chunks**: 5

## Troubleshooting

### Common Issues

1. **No PDF files found**
   ```bash
   # Make sure PDFs are in the documents folder
   ls documents/
   # Should show .pdf files
   ```

2. **Ollama Connection Error**
   ```bash
   # Check if Ollama is running
   ollama serve
   # In another terminal
   ollama list
   ```

3. **Model Not Found**
   ```bash
   # Install DeepSeek-R1 model
   ollama pull deepseek-r1:latest
   ```

4. **Empty Documents Folder**
   - Add PDF files to `./documents/` folder
   - Ensure PDFs are not password protected
   - Check file permissions

### Logs
Check log files in `./logs/rag_system.log` for detailed error information.

## Tips for Better Results

1. **Document Quality**: Use text-based PDFs (not scanned images)
2. **File Organization**: Put related documents together
3. **Question Clarity**: Ask specific, clear questions
4. **Multiple Documents**: The system works better with multiple related PDFs
5. **File Size**: Keep PDFs under 50MB for best performance