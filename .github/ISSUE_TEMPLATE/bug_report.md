---
name: Bug Report
about: Create a report to help us improve pyresume
title: '[BUG] '
labels: 'bug'
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Import pyresume with '...'
2. Parse resume with '...'
3. Call method '...'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Code sample**
```python
# Minimal code sample that reproduces the issue
from pyresume import ResumeParser

parser = ResumeParser()
# ... your code here
```

**Error message**
If applicable, paste the full error message/traceback:
```
Paste error message here
```

**Sample resume file (if applicable)**
If the issue is related to parsing a specific resume format, please:
- [ ] Attach a sample resume file (remove personal information)
- [ ] Describe the file format (PDF, DOCX, TXT)
- [ ] Mention any special formatting or structure

**Environment (please complete the following information):**
- OS: [e.g. Windows 10, macOS 12.0, Ubuntu 20.04]
- Python version: [e.g. 3.9.5]
- pyresume version: [e.g. 0.1.0]
- Dependency versions:
  - pdfplumber: [if using PDF parsing]
  - python-docx: [if using DOCX parsing]
  - Other relevant packages

**Additional context**
Add any other context about the problem here. For example:
- Does this happen with all resume files or specific ones?
- Did this work in a previous version?
- Any workarounds you've found?

**Privacy note**
Please ensure any sample files or text you share do not contain personal information. Remove or redact names, contact details, companies, etc.