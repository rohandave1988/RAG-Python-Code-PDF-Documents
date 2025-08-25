# Quick Usage Guide

## 🚀 Running the RAG System

### Interactive Demo (Recommended)
```bash
python apps/rag_demo.py
```

### Command Line Interface
```bash
# Show system status
python apps/main.py --status

# Index documents from a directory
python apps/main.py --index ./documents

# Ask a question
python apps/main.py --query "What is artificial intelligence?"

# Ask with custom settings
python apps/main.py --query "How does ML work?" --top-k 3
```

## 📦 Project Structure

```
RAG-Python-Code/
├── 🚀 apps/                       # Application entry points
│   ├── main.py                    # CLI application
│   └── rag_demo.py               # Interactive demo
│
├── 📦 indexing/                   # Document processing
├── 🔍 searching/                  # Query & response generation  
├── ⚙️ config/                     # Configuration management
├── 🛠️ utils/                      # Shared utilities
├── 📄 docs/                      # Documentation
│
├── 📁 documents/                  # Place PDF files here
├── 🗃️ vector_db/                  # Database storage
└── 📋 requirements.txt            # Dependencies
```

## 🎯 Key Features

- **Document Indexing**: PDF processing with intelligent chunking
- **Smart Search**: Vector similarity search with semantic understanding
- **AI Responses**: Context-aware answer generation using LLMs
- **Multiple Interfaces**: Both CLI and interactive demo modes
- **Modular Design**: Clean package separation for easy maintenance

## 🔧 Quick Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Start Ollama: `ollama serve`
3. Install model: `ollama pull deepseek-r1:latest`
4. Add PDFs to `./documents/` folder
5. Run demo: `python apps/rag_demo.py`

---
**Ready to explore your documents with AI! 🤖📚**