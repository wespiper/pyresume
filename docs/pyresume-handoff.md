# PyResume - Repository Handoff Document

## Overview
This document provides all the context needed to create the `pyresume` open-source resume parser library as a standalone repository.

## Project Background

### Origin Story
- **Parent Project**: ATS Intelligence System
- **Problem**: Lever's public resume parsing API now requires authentication (403 errors)
- **Solution**: Build our own open-source resume parser that rivals commercial solutions
- **Philosophy**: Simple, importable Python library - no services, just good parsing

### Key Decisions Made
1. **Name**: `pyresume` - Pythonic, clear, follows conventions like pytest/pyyaml
2. **License**: MIT License for maximum adoption
3. **Approach**: Library-first, no hosted services or complex infrastructure
4. **Philosophy**: 100% open source, no proprietary features

## Technical Specifications

### Core API Design
```python
from pyresume import ResumeParser

# Basic usage
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

### Supported File Formats
- PDF (using pdfplumber)
- DOCX (using python-docx)
- DOC (with fallback conversion)
- TXT
- RTF (stretch goal)

### Data Model
```python
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

## Repository Structure
```
pyresume/
├── README.md
├── LICENSE
├── setup.py
├── requirements.txt
├── requirements-dev.txt
├── .gitignore
├── .github/
│   ├── workflows/
│   │   ├── tests.yml
│   │   └── release.yml
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       └── feature_request.md
├── pyresume/
│   ├── __init__.py
│   ├── parser.py
│   ├── extractors/
│   │   ├── __init__.py
│   │   ├── pdf.py
│   │   ├── docx.py
│   │   └── text.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── resume.py
│   └── utils/
│       ├── __init__.py
│       ├── dates.py
│       ├── phones.py
│       └── patterns.py
├── tests/
│   ├── __init__.py
│   ├── fixtures/
│   │   ├── sample.pdf
│   │   ├── sample.docx
│   │   └── sample.txt
│   ├── test_parser.py
│   ├── test_extractors.py
│   └── test_utils.py
├── examples/
│   ├── basic_usage.py
│   ├── batch_processing.py
│   └── confidence_scores.py
└── docs/
    ├── getting_started.md
    ├── api_reference.md
    └── contributing.md
```

## Initial Implementation Plan

### Phase 1: MVP (Week 1)
1. Set up repository structure
2. Implement basic PDF text extraction
3. Create Resume data model
4. Add simple regex-based email/phone extraction
5. Basic section detection (Experience, Education)
6. Initial test suite

### Phase 2: Enhanced Parsing (Week 2)
1. Add DOCX support
2. Improve section detection algorithm
3. Add date parsing utilities
4. Implement skills extraction
5. Add confidence scoring

### Phase 3: Polish & Release (Week 3)
1. Comprehensive documentation
2. Example scripts
3. CI/CD setup
4. PyPI package configuration
5. Initial release

## Key Technical Details

### Dependencies (Minimal)
```python
# setup.py
install_requires=[
    "pdfplumber>=0.10.0",
    "python-docx>=1.0.0",
    "python-dateutil>=2.8.0",
    "phonenumbers>=8.13.0",
]
```

### Parsing Strategy
1. **Text Extraction**: Format-specific extractors
2. **Section Detection**: Keyword and pattern matching
3. **Entity Extraction**: Regex + validation
4. **Date Normalization**: Flexible date parsing
5. **Confidence Scoring**: Track extraction confidence

### Testing Approach
- Unit tests for each component
- Integration tests with real resume samples
- Property-based testing for edge cases
- Benchmark against known good parses

## Integration with ATS Intelligence

The ATS Intelligence system will use pyresume as a dependency:

```python
# In ATS Intelligence requirements.txt
pyresume>=1.0.0

# In ATS Intelligence code
from pyresume import ResumeParser

class ResumeService:
    def __init__(self):
        self.parser = ResumeParser()
    
    def process_resume(self, file_path: str):
        resume = self.parser.parse(file_path)
        # Further processing for ATS simulation
        return self.enhance_with_ats_insights(resume)
```

## Success Metrics

### Technical Goals
- 95%+ accuracy on contact information
- 90%+ accuracy on experience extraction  
- <2 second parse time for typical resumes
- Support for 95%+ of real-world resume formats

### Community Goals
- 100+ GitHub stars in first month
- 10+ contributors in first 3 months
- 1000+ monthly PyPI downloads
- Active issue discussions

## Marketing & Launch

### Launch Checklist
- [ ] Create GitHub repository
- [ ] Implement MVP features
- [ ] Write comprehensive README
- [ ] Create documentation site
- [ ] Publish to PyPI
- [ ] Write launch blog post
- [ ] Post on Reddit (r/Python, r/programming)
- [ ] Share on Hacker News
- [ ] Tweet announcement
- [ ] Create demo video

### Key Messages
- "Simple, accurate resume parsing for Python"
- "No services, no complexity, just `pip install pyresume`"
- "Open source alternative to expensive parsing APIs"
- "Built by developers, for developers"

## Useful Resources

### Research & Context
- Original ATS Intelligence research: `/docs/plans/ats-intelligence-overview.md`
- Custom parser plan: `/docs/plans/custom-parser-plan.md`
- Simple library design: `/docs/plans/simple-parser-library.md`

### Technical References
- Lever API (for comparison): Previously at `https://jobs.lever.co/parseResume`
- ATS scoring algorithms: See ATS Intelligence research doc
- Common resume formats and patterns: Industry knowledge

### Example Code to Port
Look at `/services/resume-parser/parsers/lever_parser.py` for:
- Error handling patterns
- Caching strategies (though pyresume won't include caching)
- Response formatting

## Next Steps

1. **Create Repository**
   ```bash
   # Create new repo at github.com/[username]/pyresume
   git clone https://github.com/[username]/pyresume
   cd pyresume
   ```

2. **Initialize Project**
   ```bash
   # Set up Python project
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -e .
   ```

3. **Start with Core**
   - Copy this handoff doc to the repo for reference
   - Create basic project structure
   - Implement PDF text extraction first
   - Add tests as you go

## Questions to Answer Early

1. **OCR Support**: Include by default or as optional dependency?
2. **ML Features**: Start simple or include NLP from day 1?
3. **Benchmarking**: What resume dataset to use for accuracy testing?
4. **API Compatibility**: Match any existing parser API for easy migration?

## Contact & Support

When pyresume is successful and widely adopted, it will enhance the credibility of the ATS Intelligence system as a technical leader in the resume optimization space.

Remember: Keep it simple, make it work, then make it better. The open source community will help with the rest!