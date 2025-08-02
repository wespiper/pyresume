"""
DOCX text extraction using python-docx.
"""
from typing import Optional

try:
    from docx import Document
except ImportError:
    Document = None


class DOCXExtractor:
    """Extract text content from DOCX files."""
    
    def __init__(self):
        if Document is None:
            raise ImportError("python-docx is required for DOCX extraction. Install with: pip install python-docx")
    
    def extract_text(self, file_path: str) -> str:
        """
        Extract text content from a DOCX file.
        
        Args:
            file_path: Path to the DOCX file
            
        Returns:
            Extracted text content
            
        Raises:
            Exception: If DOCX cannot be read or processed
        """
        try:
            doc = Document(file_path)
            text_parts = []
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_parts.append(paragraph.text)
            
            # Extract text from tables
            for table in doc.tables:
                for row in table.rows:
                    row_text = []
                    for cell in row.cells:
                        if cell.text.strip():
                            row_text.append(cell.text.strip())
                    if row_text:
                        text_parts.append(' | '.join(row_text))
            
            return '\n'.join(text_parts)
            
        except Exception as e:
            raise Exception(f"Failed to extract text from DOCX: {str(e)}")
    
    def extract_structure(self, file_path: str) -> dict:
        """
        Extract document structure (headings, tables, etc.) for future enhancement.
        
        Args:
            file_path: Path to the DOCX file
            
        Returns:
            Dictionary containing document structure information
        """
        # TODO: Implement structure extraction for better parsing
        return {}