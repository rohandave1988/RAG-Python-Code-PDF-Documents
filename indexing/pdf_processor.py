"""
Simplified PDF processing module.
"""

import pdfplumber

class PDFProcessor:
    """Simple PDF text extraction."""
    
    def extract_text(self, pdf_path: str) -> str:
        """Extract text from PDF."""
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    
    def extract_text_with_metadata(self, pdf_path: str) -> dict:
        """Extract text from PDF with metadata."""
        try:
            text = self.extract_text(pdf_path)
            return {
                "success": True,
                "text": text,
                "metadata": {
                    "filename": pdf_path,
                    "page_count": 0,  # Simplified
                    "file_size": 0    # Simplified
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }