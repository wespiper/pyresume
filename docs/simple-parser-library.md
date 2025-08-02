# OpenResumeParser - Simple Library Design

## Philosophy
A lightweight, dependency-minimal Python library for parsing resumes. Just import and use.

## Simple API Design

### Basic Usage
```python
from openresumeparser import ResumeParser

# Parse a resume
parser = ResumeParser()
resume = parser.parse("path/to/resume.pdf")

# Access parsed data
print(resume.name)
print(resume.email)
print(resume.phone)
print(resume.experience)
print(resume.education)
print(resume.skills)
```

### Advanced Usage
```python
# With configuration
parser = ResumeParser(
    extract_contact=True,
    extract_experience=True,
    extract_education=True,
    extract_skills=True,
    use_ocr=True
)

# Parse with custom date formats
parser.date_formats = ["%B %Y", "%m/%Y", "%Y-%m-%d"]
resume = parser.parse("resume.pdf")

# Get parsing confidence scores
print(resume.confidence_scores)

# Get raw extracted text
print(resume.raw_text)
```

## Library Structure
```
openresumeparser/
├── __init__.py
├── parser.py           # Main parser class
├── extractors/         # File format handlers
│   ├── __init__.py
│   ├── pdf.py
│   ├── docx.py
│   └── text.py
├── models/             # Data models
│   ├── __init__.py
│   └── resume.py
├── utils/              # Utilities
│   ├── __init__.py
│   ├── dates.py
│   ├── phones.py
│   └── patterns.py
└── data/               # Static data
    └── skills.json     # Common skills list
```

## Core Implementation

### Main Parser Class
```python
# openresumeparser/parser.py
from typing import Union, Dict, Any
from pathlib import Path

class ResumeParser:
    def __init__(self, **config):
        self.config = config
        
    def parse(self, file_path: Union[str, Path]) -> Resume:
        """Parse a resume file and return structured data"""
        # 1. Detect file type
        # 2. Extract text
        # 3. Parse sections
        # 4. Extract entities
        # 5. Return Resume object
        pass
    
    def parse_text(self, text: str) -> Resume:
        """Parse already extracted text"""
        pass
```

### Resume Model
```python
# openresumeparser/models/resume.py
from dataclasses import dataclass
from typing import List, Optional, Dict

@dataclass
class Experience:
    company: str
    title: str
    start_date: Optional[str]
    end_date: Optional[str]
    description: List[str]

@dataclass
class Education:
    institution: str
    degree: str
    field: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    gpa: Optional[float]

@dataclass
class Resume:
    # Contact Information
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    location: Optional[str]
    linkedin: Optional[str]
    github: Optional[str]
    
    # Content
    summary: Optional[str]
    experience: List[Experience]
    education: List[Education]
    skills: List[str]
    
    # Metadata
    raw_text: str
    file_path: Optional[str]
    confidence_scores: Dict[str, float]
```

## Installation

```bash
# From PyPI
pip install openresumeparser

# From source
git clone https://github.com/yourusername/openresumeparser
cd openresumeparser
pip install -e .
```

## Dependencies (Minimal)
```python
# setup.py
setup(
    name="openresumeparser",
    install_requires=[
        "pdfplumber>=0.10.0",  # PDF extraction
        "python-docx>=1.0.0",  # DOCX extraction
        "python-dateutil>=2.8.0",  # Date parsing
        "phonenumbers>=8.13.0",  # Phone parsing
    ],
    extras_require={
        "ocr": ["pytesseract>=0.3.0"],  # Optional OCR
        "ml": ["spacy>=3.7.0"],  # Optional ML features
    }
)
```

## Features

### Core Features (Always Included)
- PDF text extraction
- DOCX text extraction
- Contact information parsing (name, email, phone)
- Experience section detection
- Education section detection
- Skills extraction
- Date normalization

### Optional Features (Install Extras)
- OCR for scanned documents (`pip install openresumeparser[ocr]`)
- ML-enhanced parsing (`pip install openresumeparser[ml]`)

## Example Integration with ATS Intelligence

```python
# In ATS Intelligence
from openresumeparser import ResumeParser

class ResumeService:
    def __init__(self):
        self.parser = ResumeParser()
    
    def process_resume(self, file_path: str) -> dict:
        # Parse resume
        resume = self.parser.parse(file_path)
        
        # Convert to our internal format
        return {
            "contact": {
                "name": resume.name,
                "email": resume.email,
                "phone": resume.phone,
            },
            "experience": [
                {
                    "company": exp.company,
                    "title": exp.title,
                    "duration": exp.start_date + " - " + exp.end_date,
                    "description": exp.description
                }
                for exp in resume.experience
            ],
            "skills": resume.skills,
            # ... rest of the mapping
        }
```

## Testing

```python
# tests/test_parser.py
import pytest
from openresumeparser import ResumeParser

def test_pdf_parsing():
    parser = ResumeParser()
    resume = parser.parse("tests/fixtures/sample.pdf")
    
    assert resume.name is not None
    assert resume.email is not None
    assert len(resume.experience) > 0

def test_docx_parsing():
    parser = ResumeParser()
    resume = parser.parse("tests/fixtures/sample.docx")
    
    assert resume.name is not None
    assert resume.email is not None
```

## Documentation

### README.md
```markdown
# OpenResumeParser

A simple, accurate resume parser for Python.

## Installation
```bash
pip install openresumeparser
```

## Quick Start
```python
from openresumeparser import ResumeParser

parser = ResumeParser()
resume = parser.parse("resume.pdf")

print(f"Name: {resume.name}")
print(f"Email: {resume.email}")
print(f"Skills: {', '.join(resume.skills)}")
```

## Features
- 📄 Supports PDF, DOCX, TXT formats
- 🎯 High accuracy entity extraction
- 🚀 Fast and lightweight
- 🔧 Minimal dependencies
- 🐍 Pure Python implementation
```

## Benefits of Simple Library Approach

1. **Easy to Use**: Import and go, no services to run
2. **Lightweight**: Minimal dependencies
3. **Flexible**: Use it however you want
4. **Testable**: Easy to unit test
5. **Maintainable**: Simple codebase
6. **Portable**: Works anywhere Python works

## What We're NOT Building
- ❌ No API service
- ❌ No Docker requirements
- ❌ No database
- ❌ No authentication
- ❌ No rate limiting
- ❌ No hosted solution

## Just a Good Parser
Focus on doing one thing really well: parsing resumes into structured data.