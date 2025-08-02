"""
Tests for the main ResumeParser class.
"""
import pytest
from pathlib import Path
from datetime import date
from pyresume.parser import ResumeParser
from pyresume.models.resume import Resume


class TestResumeParser:
    """Test cases for ResumeParser."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.parser = ResumeParser()
        # Get the fixtures directory path
        self.fixtures_dir = Path(__file__).parent / "fixtures"
    
    def test_parser_initialization(self):
        """Test parser initializes with correct extractors."""
        assert '.pdf' in self.parser.extractors
        assert '.docx' in self.parser.extractors
        assert '.txt' in self.parser.extractors
    
    def test_parse_nonexistent_file(self):
        """Test parsing a non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            self.parser.parse('/nonexistent/file.pdf')
    
    def test_parse_unsupported_format(self, tmp_path):
        """Test parsing unsupported file format raises ValueError."""
        # Create a file with unsupported extension
        test_file = tmp_path / "test.xyz"
        test_file.write_text("some content")
        
        with pytest.raises(ValueError, match="Unsupported file format"):
            self.parser.parse(str(test_file))
    
    def test_parse_text_returns_resume(self):
        """Test parsing text returns Resume object."""
        test_text = "John Doe\njohn@example.com\nSoftware Engineer"
        result = self.parser.parse_text(test_text)
        
        assert isinstance(result, Resume)
        assert result.raw_text == test_text
    
    def test_parse_empty_text(self):
        """Test parsing empty text."""
        result = self.parser.parse_text("")
        assert isinstance(result, Resume)
        assert result.raw_text == ""
    
    @pytest.mark.integration
    def test_parse_text_file(self, tmp_path):
        """Integration test for parsing a text file."""
        # Create a sample resume text file
        test_content = """John Doe
john.doe@email.com
(555) 123-4567

EXPERIENCE
Software Engineer at Tech Corp
Jan 2020 - Present
- Developed web applications
- Led team of 5 developers

EDUCATION
Bachelor of Science in Computer Science
University of Technology
2016 - 2020
"""
        
        test_file = tmp_path / "resume.txt"
        test_file.write_text(test_content)
        
        result = self.parser.parse(str(test_file))
        assert isinstance(result, Resume)
        assert result.raw_text == test_content

    @pytest.mark.integration
    def test_parse_standard_resume(self):
        """Test parsing a standard well-formatted resume."""
        resume_file = self.fixtures_dir / "resume_standard.txt"
        result = self.parser.parse(str(resume_file))
        
        assert isinstance(result, Resume)
        assert result.contact_info.name == "John Smith"
        assert result.contact_info.email == "john.smith@email.com"
        assert result.contact_info.phone == "(555) 123-4567"
        assert result.contact_info.linkedin == "https://linkedin.com/in/johnsmith"
        assert result.contact_info.github == "https://github.com/johnsmith"
        
        # Check experience extraction
        assert len(result.experience) >= 2
        senior_eng = next((exp for exp in result.experience if "Senior Software Engineer" in (exp.title or "")), None)
        assert senior_eng is not None
        assert senior_eng.company == "Google Inc."
        assert senior_eng.location == "Mountain View, CA"
        assert senior_eng.current is True
        
        # Check education extraction
        assert len(result.education) >= 1
        education = result.education[0]
        assert "Bachelor of Science" in (education.degree or "")
        assert "University of California, Berkeley" in (education.institution or "")
        assert education.gpa == "3.8/4.0"
        
        # Check skills extraction
        assert len(result.skills) > 0
        skill_names = [skill.name.lower() for skill in result.skills]
        assert any("python" in name for name in skill_names)
        assert any("javascript" in name for name in skill_names)
        
        # Check projects
        assert len(result.projects) >= 1
        
        # Check certifications
        assert len(result.certifications) >= 1
        aws_cert = next((cert for cert in result.certifications if "AWS" in (cert.name or "")), None)
        assert aws_cert is not None
        
        # Check overall confidence
        assert result.extraction_metadata['overall_confidence'] > 0.5

    @pytest.mark.integration
    def test_parse_minimal_resume(self):
        """Test parsing a minimal resume with basic information."""
        resume_file = self.fixtures_dir / "resume_minimal.txt"
        result = self.parser.parse(str(resume_file))
        
        assert isinstance(result, Resume)
        assert result.contact_info.name == "Jane Doe"
        assert result.contact_info.email == "jane.doe@gmail.com"
        assert result.contact_info.phone == "(415) 987-6543"
        
        # Should extract at least some experience
        assert len(result.experience) >= 1
        
        # Should extract education
        assert len(result.education) >= 1
        education = result.education[0]
        assert "Computer Science" in (education.degree or education.major or "")
        
        # Should extract some skills
        assert len(result.skills) > 0

    @pytest.mark.integration
    def test_parse_complex_resume(self):
        """Test parsing a complex resume with advanced formatting."""
        resume_file = self.fixtures_dir / "resume_complex.txt"
        result = self.parser.parse(str(resume_file))
        
        assert isinstance(result, Resume)
        assert "ALEXANDRA MARTINEZ-CHEN" in (result.contact_info.name or "")
        assert result.contact_info.email == "a.martinez.chen@university.edu"
        
        # Complex resume should have multiple experiences
        assert len(result.experience) >= 3
        
        # Should have multiple education entries
        assert len(result.education) >= 2
        phd = next((edu for edu in result.education if "Ph.D" in (edu.degree or "")), None)
        assert phd is not None
        assert "MIT" in (phd.institution or "") or "Massachusetts Institute" in (phd.institution or "")
        
        # Should extract many skills from technical expertise section
        assert len(result.skills) >= 10
        
        # Should have high confidence due to well-structured content
        assert result.extraction_metadata['overall_confidence'] > 0.6

    @pytest.mark.integration
    def test_parse_edge_cases_resume(self):
        """Test parsing a resume with various edge cases and formatting quirks."""
        resume_file = self.fixtures_dir / "resume_edge_cases.txt"
        result = self.parser.parse(str(resume_file))
        
        assert isinstance(result, Resume)
        # Name with special characters and titles
        assert "BOB" in (result.contact_info.name or "").upper()
        assert "O'CONNOR" in (result.contact_info.name or "").upper()
        
        # Email with plus sign
        assert "bob.oconnor+resume@gmail.com" == result.contact_info.email
        
        # Phone with extension
        assert "555" in (result.contact_info.phone or "")
        
        # Should handle complex experience entries with detailed descriptions
        assert len(result.experience) >= 3
        
        # Should extract education in progress
        assert len(result.education) >= 2
        masters = next((edu for edu in result.education if "Master" in (edu.degree or "")), None)
        assert masters is not None
        
        # Should extract certifications with expiry dates
        assert len(result.certifications) >= 1

    @pytest.mark.integration
    def test_parse_international_resume(self):
        """Test parsing an international resume with non-English content."""
        resume_file = self.fixtures_dir / "resume_international.txt"
        result = self.parser.parse(str(resume_file))
        
        assert isinstance(result, Resume)
        assert "MARIE-CLAIRE DUBOIS" in (result.contact_info.name or "")
        assert result.contact_info.email == "marie.claire.dubois@email.fr"
        
        # Should extract some experience even with French text
        assert len(result.experience) >= 1
        
        # Should extract education
        assert len(result.education) >= 1
        
        # Should extract some skills despite different language
        assert len(result.skills) > 0

    def test_parse_empty_resume(self):
        """Test parsing an empty resume file."""
        resume_file = self.fixtures_dir / "resume_empty.txt"
        result = self.parser.parse(str(resume_file))
        
        assert isinstance(result, Resume)
        assert result.raw_text == ""
        assert result.extraction_metadata['overall_confidence'] == 0.0

    def test_parse_malformed_resume(self):
        """Test parsing a malformed resume with poor structure."""
        resume_file = self.fixtures_dir / "resume_malformed.txt"
        result = self.parser.parse(str(resume_file))
        
        assert isinstance(result, Resume)
        # Should still return a Resume object even with poor content
        assert result.extraction_metadata['overall_confidence'] >= 0.0
        # May or may not extract meaningful data, but shouldn't crash

    def test_confidence_scoring(self):
        """Test that confidence scores are properly calculated."""
        # Test with good content
        good_text = """John Smith
john@email.com
(555) 123-4567

EXPERIENCE
Software Engineer at Google
2020 - Present

EDUCATION
BS Computer Science
MIT
2020
"""
        result = self.parser.parse_text(good_text)
        assert result.extraction_metadata['overall_confidence'] > 0.4
        
        # Test with poor content
        poor_text = "random text with no structure"
        result_poor = self.parser.parse_text(poor_text)
        assert result_poor.extraction_metadata['overall_confidence'] < 0.3

    def test_extraction_metadata(self):
        """Test that extraction metadata is properly populated."""
        test_text = """John Doe
john@example.com
Software Engineer
"""
        result = self.parser.parse_text(test_text)
        
        metadata = result.extraction_metadata
        assert 'text_length' in metadata
        assert 'lines_count' in metadata
        assert 'has_email' in metadata
        assert 'has_name' in metadata
        assert 'overall_confidence' in metadata
        
        assert metadata['text_length'] == len(test_text)
        assert metadata['has_email'] is True

    def test_date_extraction_accuracy(self):
        """Test accuracy of date extraction in experience."""
        text_with_dates = """John Doe
john@example.com

EXPERIENCE
Software Engineer at TechCorp
January 2020 - March 2022
- Did software things

Senior Developer at WebCorp  
Apr 2022 - Present
- Lead development team
"""
        result = self.parser.parse_text(text_with_dates)
        
        assert len(result.experience) >= 2
        
        # Find the experiences and check dates
        techcorp_exp = next((exp for exp in result.experience if "TechCorp" in (exp.company or "")), None)
        if techcorp_exp:
            assert techcorp_exp.start_date == date(2020, 1, 1)
            assert techcorp_exp.end_date == date(2022, 3, 1)
            assert techcorp_exp.current is False
        
        webcorp_exp = next((exp for exp in result.experience if "WebCorp" in (exp.company or "")), None)
        if webcorp_exp:
            assert webcorp_exp.start_date == date(2022, 4, 1)
            assert webcorp_exp.current is True

    def test_skills_categorization(self):
        """Test that skills are properly categorized."""
        text_with_skills = """John Doe
john@example.com

SKILLS
Programming Languages: Python, JavaScript, Java
Databases: PostgreSQL, MongoDB
Cloud: AWS, Docker, Kubernetes
"""
        result = self.parser.parse_text(text_with_skills)
        
        assert len(result.skills) > 0
        
        # Check that skills have categories
        skill_categories = {skill.category for skill in result.skills if skill.category}
        assert len(skill_categories) > 0
        
        # Check specific categorizations
        python_skill = next((skill for skill in result.skills if "python" in skill.name.lower()), None)
        if python_skill:
            assert python_skill.category == "programming"