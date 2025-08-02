"""
Tests for file format extractors.
"""
import pytest
from pathlib import Path
from pyresume.extractors.text import TextExtractor
from pyresume.extractors.pdf import PDFExtractor
from pyresume.extractors.docx import DOCXExtractor


class TestTextExtractor:
    """Test cases for TextExtractor."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.extractor = TextExtractor()
        self.fixtures_dir = Path(__file__).parent / "fixtures"
    
    def test_extract_text_from_file(self, tmp_path):
        """Test extracting text from a text file."""
        test_content = "This is a test resume\nJohn Doe\nSoftware Engineer"
        test_file = tmp_path / "resume.txt"
        test_file.write_text(test_content, encoding='utf-8')
        
        result = self.extractor.extract_text(str(test_file))
        assert result == test_content
    
    def test_extract_text_nonexistent_file(self):
        """Test extracting from non-existent file raises exception."""
        with pytest.raises(Exception):
            self.extractor.extract_text('/nonexistent/file.txt')
    
    def test_clean_text(self):
        """Test text cleaning functionality."""
        messy_text = "  Line 1  \n\n\n  Line 2  \n\n  Line 3  \n\n\n"
        cleaned = self.extractor.clean_text(messy_text)
        
        lines = cleaned.split('\n')
        # Should remove excessive whitespace but preserve structure
        assert 'Line 1' in cleaned
        assert 'Line 2' in cleaned
        assert 'Line 3' in cleaned
        # Should not have excessive blank lines
        assert '\n\n\n' not in cleaned
    
    def test_extract_text_with_encoding_issues(self, tmp_path):
        """Test handling files with encoding issues."""
        # Create file with special characters
        test_content = "Résumé for José García"
        test_file = tmp_path / "resume_special.txt"
        test_file.write_text(test_content, encoding='utf-8')
        
        result = self.extractor.extract_text(str(test_file))
        assert "José García" in result
    
    def test_extract_text_from_fixtures(self):
        """Test extracting text from fixture files."""
        # Test standard resume
        standard_file = self.fixtures_dir / "resume_standard.txt"
        result = self.extractor.extract_text(str(standard_file))
        assert "JOHN SMITH" in result
        assert "john.smith@email.com" in result
        
        # Test minimal resume
        minimal_file = self.fixtures_dir / "resume_minimal.txt"
        result = self.extractor.extract_text(str(minimal_file))
        assert "Jane Doe" in result
        assert "jane.doe@gmail.com" in result
    
    def test_extract_empty_file(self, tmp_path):
        """Test extracting from empty file."""
        empty_file = tmp_path / "empty.txt"
        empty_file.write_text("", encoding='utf-8')
        
        result = self.extractor.extract_text(str(empty_file))
        assert result == ""
    
    def test_extract_file_with_only_whitespace(self, tmp_path):
        """Test extracting from file with only whitespace."""
        whitespace_file = tmp_path / "whitespace.txt"
        whitespace_file.write_text("   \n\n\t  \n   ", encoding='utf-8')
        
        result = self.extractor.extract_text(str(whitespace_file))
        cleaned = self.extractor.clean_text(result)
        assert cleaned.strip() == ""
    
    def test_extract_large_file(self, tmp_path):
        """Test extracting from a large text file."""
        # Create a large file with repeated content
        large_content = "\n".join([f"Line {i}: This is a long line with various content about resume parsing." for i in range(1000)])
        large_file = tmp_path / "large_resume.txt"
        large_file.write_text(large_content, encoding='utf-8')
        
        result = self.extractor.extract_text(str(large_file))
        assert "Line 1:" in result
        assert "Line 999:" in result
        assert len(result.split('\n')) == 1000
    
    def test_clean_text_edge_cases(self):
        """Test text cleaning with edge cases."""
        # Test with various whitespace patterns
        test_cases = [
            ("", ""),
            ("   ", ""),
            ("\n\n\n", ""),
            ("Line1\n\n\nLine2", "Line1\n\nLine2"),
            ("  Leading spaces", "Leading spaces"),
            ("Trailing spaces  ", "Trailing spaces"),
            ("\tTabs and spaces \t", "Tabs and spaces"),
            ("Multiple\n\n\n\nNewlines", "Multiple\n\nNewlines"),
        ]
        
        for input_text, expected in test_cases:
            result = self.extractor.clean_text(input_text)
            assert result == expected or result.strip() == expected.strip()
    
    def test_file_encoding_detection(self, tmp_path):
        """Test handling different file encodings."""
        # Test UTF-8 with BOM
        utf8_bom_content = "John Doe\nSoftware Engineer"
        utf8_bom_file = tmp_path / "utf8_bom.txt"
        utf8_bom_file.write_text(utf8_bom_content, encoding='utf-8-sig')
        
        result = self.extractor.extract_text(str(utf8_bom_file))
        assert "John Doe" in result
        assert "Software Engineer" in result
        
        # Test Latin-1 encoding
        latin1_content = "Café résumé"
        latin1_file = tmp_path / "latin1.txt"
        latin1_file.write_text(latin1_content, encoding='latin-1')
        
        # Should handle encoding gracefully
        result = self.extractor.extract_text(str(latin1_file))
        assert len(result) > 0  # Should not crash


class TestPDFExtractor:
    """Test cases for PDFExtractor."""
    
    def setup_method(self):
        """Set up test fixtures."""
        try:
            self.extractor = PDFExtractor()
            self.pdf_available = True
        except ImportError:
            self.pdf_available = False
            pytest.skip("pdfplumber not available")
    
    def test_pdf_extractor_initialization(self):
        """Test that PDFExtractor initializes correctly when pdfplumber is available."""
        if self.pdf_available:
            assert self.extractor is not None
    
    def test_pdf_extractor_import_error_handling(self):
        """Test handling when pdfplumber is not available."""
        # This test checks that the import error is properly handled
        # when pdfplumber is not installed
        try:
            from pyresume.extractors.pdf import PDFExtractor
            PDFExtractor()
        except ImportError as e:
            assert "pdfplumber" in str(e)
    
    def test_extract_text_from_nonexistent_pdf(self):
        """Test extracting from non-existent PDF raises exception."""
        if self.pdf_available:
            with pytest.raises(Exception):
                self.extractor.extract_text('/nonexistent/file.pdf')
    
    def test_extract_text_invalid_pdf(self, tmp_path):
        """Test extracting from invalid PDF file."""
        if self.pdf_available:
            # Create a file that's not actually a PDF
            fake_pdf = tmp_path / "fake.pdf"
            fake_pdf.write_text("This is not a PDF file")
            
            with pytest.raises(Exception):
                self.extractor.extract_text(str(fake_pdf))
    
    def test_clean_text_pdf_specific(self):
        """Test PDF-specific text cleaning."""
        if self.pdf_available and hasattr(self.extractor, 'clean_text'):
            # Test cleaning text that might come from PDF extraction
            pdf_text = "John  Doe\n\nSoftware   Engineer\n\n\nExperience:\n• Bullet  point\n• Another   point"
            cleaned = self.extractor.clean_text(pdf_text)
            
            assert "John" in cleaned
            assert "Software" in cleaned
            assert "Engineer" in cleaned


class TestDOCXExtractor:
    """Test cases for DOCXExtractor."""
    
    def setup_method(self):
        """Set up test fixtures."""
        try:
            self.extractor = DOCXExtractor()
            self.docx_available = True
        except ImportError:
            self.docx_available = False
            pytest.skip("python-docx not available")
    
    def test_docx_extractor_initialization(self):
        """Test that DOCXExtractor initializes correctly when python-docx is available."""
        if self.docx_available:
            assert self.extractor is not None
    
    def test_docx_extractor_import_error_handling(self):
        """Test handling when python-docx is not available."""
        # This test checks that the import error is properly handled
        # when python-docx is not installed
        try:
            from pyresume.extractors.docx import DOCXExtractor
            DOCXExtractor()
        except ImportError as e:
            assert "python-docx" in str(e) or "docx" in str(e)
    
    def test_extract_text_from_nonexistent_docx(self):
        """Test extracting from non-existent DOCX raises exception."""
        if self.docx_available:
            with pytest.raises(Exception):
                self.extractor.extract_text('/nonexistent/file.docx')
    
    def test_extract_text_invalid_docx(self, tmp_path):
        """Test extracting from invalid DOCX file."""
        if self.docx_available:
            # Create a file that's not actually a DOCX
            fake_docx = tmp_path / "fake.docx"
            fake_docx.write_text("This is not a DOCX file")
            
            with pytest.raises(Exception):
                self.extractor.extract_text(str(fake_docx))
    
    def test_clean_text_docx_specific(self):
        """Test DOCX-specific text cleaning."""
        if self.docx_available and hasattr(self.extractor, 'clean_text'):
            # Test cleaning text that might come from DOCX extraction
            docx_text = "John Doe\n\nSoftware Engineer\n\n\nProfessional Experience\n\nSoftware Developer at TechCorp\n\n• Developed applications\n• Managed projects"
            cleaned = self.extractor.clean_text(docx_text)
            
            assert "John Doe" in cleaned
            assert "Software Engineer" in cleaned
            assert "Professional Experience" in cleaned


class TestExtractorEdgeCases:
    """Test edge cases that apply to all extractors."""
    
    def test_file_permission_error(self, tmp_path):
        """Test handling file permission errors."""
        # Create a file and remove read permissions (Unix only)
        import os
        import stat
        
        test_file = tmp_path / "no_permission.txt"
        test_file.write_text("test content")
        
        # Remove read permission
        try:
            os.chmod(str(test_file), stat.S_IWRITE)
            
            extractor = TextExtractor()
            with pytest.raises(PermissionError):
                extractor.extract_text(str(test_file))
        except (OSError, NotImplementedError):
            # Skip on systems that don't support chmod (like Windows)
            pytest.skip("chmod not supported on this system")
        finally:
            # Restore permissions for cleanup
            try:
                os.chmod(str(test_file), stat.S_IREAD | stat.S_IWRITE)
            except (OSError, FileNotFoundError):
                pass
    
    def test_very_long_filename(self, tmp_path):
        """Test handling very long filenames."""
        # Create a file with a very long name
        long_name = "a" * 200 + ".txt"
        try:
            test_file = tmp_path / long_name
            test_file.write_text("test content")
            
            extractor = TextExtractor()
            result = extractor.extract_text(str(test_file))
            assert result == "test content"
        except OSError:
            # Skip if filesystem doesn't support long filenames
            pytest.skip("Filesystem doesn't support long filenames")
    
    def test_file_with_special_characters_in_path(self, tmp_path):
        """Test handling files with special characters in path."""
        special_chars_dir = tmp_path / "special chars & symbols!"
        special_chars_dir.mkdir()
        
        test_file = special_chars_dir / "résumé file (copy).txt"
        test_file.write_text("Special character test content")
        
        extractor = TextExtractor()
        result = extractor.extract_text(str(test_file))
        assert "Special character test content" in result