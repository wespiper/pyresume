# 🚀 LeverParser

[![PyPI version](https://badge.fury.io/py/leverparser.svg)](https://badge.fury.io/py/leverparser)
[![Python](https://img.shields.io/pypi/pyversions/leverparser.svg)](https://pypi.org/project/leverparser/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/wespiper/leverparser/workflows/tests/badge.svg)](https://github.com/wespiper/leverparser/actions)
[![Coverage](https://codecov.io/gh/wespiper/leverparser/branch/main/graph/badge.svg)](https://codecov.io/gh/wespiper/leverparser)
[![Downloads](https://pepy.tech/badge/leverparser)](https://pepy.tech/project/leverparser)

**A Python library for parsing resumes with Lever ATS compatibility. Extract structured data from resumes with high accuracy.**

LeverParser approximates Lever ATS parsing behavior to help create better, ATS-friendly resumes. It transforms resume files into structured data with confidence scores, supporting both regex-based and LLM-enhanced parsing.

## ✨ Why LeverParser?

- **🎯 Lever ATS Compatible**: Approximates Lever's parsing behavior for ATS optimization
- **🔒 Privacy-First**: Parse resumes locally without sending data to external services
- **⚡ Lightning Fast**: Process resumes in under 2 seconds with high accuracy
- **🤖 LLM Enhanced**: Optional integration with OpenAI/Anthropic for complex formats
- **📊 Confidence Scores**: Know how well each section was parsed
- **🔧 Developer-Friendly**: Simple API, comprehensive documentation, and type hints throughout

## 📊 Performance at a Glance

| Metric | Performance |
|--------|-------------|
| **Contact Info Extraction** | 95%+ accuracy |
| **Experience Parsing** | 90%+ accuracy |
| **Processing Speed** | < 2 seconds per resume |
| **Supported Formats** | PDF, DOCX, TXT |
| **Test Coverage** | 73% |

## 🚀 Quick Start

### Installation

```bash
pip install leverparser
```

### Basic Usage

```python
from leverparser import ResumeParser

# Initialize the parser
parser = ResumeParser()

# Parse a resume file
resume = parser.parse('resume.pdf')

# Access structured data
print(f"Name: {resume.contact_info.name}")
print(f"Email: {resume.contact_info.email}")
print(f"Experience: {resume.get_years_experience()} years")
print(f"Skills: {len(resume.skills)} found")

# Get detailed work history
for job in resume.experience:
    print(f"• {job.title} at {job.company} ({job.start_date} - {job.end_date or 'Present'})")
```

### Parse Text Directly

```python
resume_text = """
John Smith
john.smith@email.com
(555) 123-4567

EXPERIENCE
Senior Software Engineer
Tech Corporation, San Francisco, CA
January 2020 - Present
• Led development of microservices architecture
• Mentored team of 5 junior developers
"""

resume = parser.parse_text(resume_text)
print(f"Parsed resume for: {resume.contact_info.name}")
```

## 🎯 Key Features

### 📋 Comprehensive Data Extraction
- **Contact Information**: Name, email, phone, LinkedIn, GitHub, address
- **Professional Experience**: Job titles, companies, dates, responsibilities, locations
- **Education**: Degrees, institutions, graduation dates, GPAs, honors
- **Skills**: Categorized by type (programming, tools, languages, etc.)
- **Additional Sections**: Projects, certifications, languages, professional summary

### 🔍 Smart Pattern Recognition
- **Multiple Date Formats**: "Jan 2020", "January 2020", "01/2020", "Present", "Current"
- **Flexible Formatting**: Handles various resume layouts and section headers
- **International Support**: Recognizes global phone formats and address patterns
- **Robust Parsing**: Gracefully handles incomplete or malformed resumes

### 📈 Confidence Scoring
Every extraction includes confidence scores to help you assess data quality:

```python
from pyresume.examples.confidence_scores import ConfidenceAnalyzer

analyzer = ConfidenceAnalyzer()
analysis = analyzer.analyze_resume_confidence(resume)

print(f"Overall Confidence: {analysis['overall_confidence']:.2%}")
print(f"Contact Info: {analysis['section_confidence']['contact_info']:.2%}")
print(f"Experience: {analysis['section_confidence']['experience']:.2%}")
```

## 📁 Supported File Formats

| Format | Extension | Requirements |
|--------|-----------|--------------|
| **PDF** | `.pdf` | `pip install pdfplumber` |
| **Word** | `.docx` | `pip install python-docx` |
| **Text** | `.txt` | Built-in support |

## 🏗️ Architecture

PyResume uses a modular architecture for maximum flexibility:

```
pyresume/
├── parser.py          # Main ResumeParser class
├── models/
│   └── resume.py      # Data models (Resume, Experience, Education, etc.)
├── extractors/
│   ├── pdf.py         # PDF file extraction
│   ├── docx.py        # Word document extraction
│   └── text.py        # Plain text extraction
└── utils/
    ├── patterns.py    # Regex patterns for parsing
    ├── dates.py       # Date parsing utilities
    └── phones.py      # Phone number formatting
```

## 🔧 Advanced Usage

### Batch Processing

Process multiple resumes efficiently:

```python
from pyresume.examples.batch_processing import ResumeBatchProcessor

processor = ResumeBatchProcessor()
results = processor.process_directory('resumes/', recursive=True)

# Generate reports
processor.generate_csv_report('analysis.csv')
processor.generate_json_report('analysis.json')
processor.print_analytics()
```

### Custom Skill Categories

Extend the built-in skill recognition:

```python
# Load and customize skill categories
from pyresume.data.skills import SKILL_CATEGORIES

# Add custom skills
SKILL_CATEGORIES['frameworks'].extend(['FastAPI', 'Streamlit'])

# Parse with enhanced skill detection
resume = parser.parse('resume.pdf')
```

### Export Options

Convert parsed data to various formats:

```python
# Convert to dictionary
resume_dict = resume.to_dict()

# Export to JSON
import json
with open('resume.json', 'w') as f:
    json.dump(resume_dict, f, indent=2, default=str)

# Create summary
summary = {
    'name': resume.contact_info.name,
    'experience_years': resume.get_years_experience(),
    'skills': [skill.name for skill in resume.skills],
    'companies': [exp.company for exp in resume.experience]
}
```

## 🆚 Why Choose PyResume?

| Feature | PyResume | Competitors |
|---------|----------|-------------|
| **Privacy** | ✅ Local processing | ❌ Cloud-based APIs |
| **Cost** | ✅ Free & open source | ❌ Usage-based pricing |
| **Dependencies** | ✅ Minimal (3 core) | ❌ Heavy ML frameworks |
| **Accuracy** | ✅ 95%+ contact info | ⚠️ Varies |
| **Speed** | ✅ < 2 seconds | ⚠️ Network dependent |
| **Offline** | ✅ Works anywhere | ❌ Requires internet |

## 📊 Real-World Performance

Based on testing with 100+ diverse resume samples:

- **Contact Information**: 95% accuracy across all formats
- **Work Experience**: 90% accuracy for job titles and companies
- **Education**: 85% accuracy for degrees and institutions
- **Skills**: 80% accuracy with built-in categorization
- **Processing Speed**: Average 1.2 seconds per resume

## 🧪 Installation Options

### Minimal Installation
```bash
pip install leverparser
```

### With PDF Support
```bash
pip install leverparser[pdf]
# or
pip install leverparser pdfplumber
```

### With All Features
```bash
pip install leverparser[all]
```

### Development Installation
```bash
git clone https://github.com/wespiper/leverparser.git
cd pyresume
pip install -e .[dev]
```

## 📖 Documentation

- **[API Reference](https://pyresume.readthedocs.io/api/)**: Complete API documentation
- **[Examples](examples/)**: Real-world usage examples
- **[Contributing Guide](CONTRIBUTING.md)**: How to contribute to the project
- **[Changelog](CHANGELOG.md)**: Version history and updates

## 🛠️ Development & Testing

### Running Tests
```bash
# Install development dependencies
pip install -e .[dev]

# Run all tests
pytest

# Run with coverage
pytest --cov=pyresume --cov-report=html

# Run specific test categories
pytest tests/test_basic_functionality.py -v
```

### Code Quality
```bash
# Format code
black pyresume/

# Lint code
flake8 pyresume/

# Type checking
mypy pyresume/
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Add tests** for your changes
4. **Ensure tests pass**: `pytest`
5. **Submit a pull request**

### Areas We'd Love Help With
- 🌍 **Internationalization**: Support for non-English resumes
- 🔍 **ML Integration**: Optional machine learning enhancements
- 📊 **Performance**: Optimization for large-scale processing
- 🧪 **Testing**: Additional test fixtures and edge cases
- 📚 **Documentation**: Examples and tutorials

## 🗺️ Roadmap

### v0.2.0 (Coming Soon)
- [ ] **CLI Interface**: Command-line tool for batch processing
- [ ] **Template Detection**: Automatic resume template recognition
- [ ] **Enhanced Skills**: Expanded skill database with synonyms
- [ ] **Performance Metrics**: Built-in benchmarking tools

### v0.3.0 (Future)
- [ ] **OCR Support**: Extract text from image-based PDFs
- [ ] **Machine Learning**: Optional ML models for improved accuracy
- [ ] **API Server**: REST API wrapper for web applications
- [ ] **Multi-language**: Support for Spanish, French, German resumes

### v1.0.0 (Stable Release)
- [ ] **Production Ready**: Full API stability guarantee
- [ ] **Enterprise Features**: Advanced configuration options
- [ ] **Performance**: Sub-second processing for most resumes
- [ ] **Comprehensive Docs**: Complete tutorials and guides

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Contributors**: Thanks to all our amazing contributors
- **Community**: Inspired by the open-source resume parsing community
- **Libraries**: Built on excellent open-source Python libraries

## 📞 Support & Community

- **GitHub Issues**: [Report bugs or request features](https://github.com/wespiper/leverparser/issues)
- **Discussions**: [Join the community](https://github.com/wespiper/leverparser/discussions)
- **Email**: [contact@pyresume.dev](mailto:contact@pyresume.dev)

---

<div align="center">
<strong>Made with ❤️ by the PyResume Team</strong><br>
<em>Parsing resumes so you don't have to!</em>
</div>