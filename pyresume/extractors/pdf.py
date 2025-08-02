"""
PDF text extraction using pdfplumber.
"""
from typing import Optional

try:
    import pdfplumber
except ImportError:
    pdfplumber = None


class PDFExtractor:
    """Extract text content from PDF files."""
    
    def __init__(self):
        if pdfplumber is None:
            raise ImportError("pdfplumber is required for PDF extraction. Install with: pip install pdfplumber")
    
    def extract_text(self, file_path: str) -> str:
        """
        Extract text content from a PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Extracted text content
            
        Raises:
            Exception: If PDF cannot be read or processed
        """
        try:
            with pdfplumber.open(file_path) as pdf:
                text_parts = []
                
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
                
                return '\n\n'.join(text_parts)
                
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    def extract_tables(self, file_path: str) -> list:
        """
        Extract tables from PDF (future enhancement).
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            List of tables found in the PDF
        """
        # TODO: Implement table extraction for structured data
        return []