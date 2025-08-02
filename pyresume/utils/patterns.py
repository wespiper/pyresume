"""
Common regex patterns and text matching utilities for resume parsing.
"""
import re
from typing import List, Dict, Pattern, Optional


class ResumePatterns:
    """Common regex patterns for extracting information from resumes."""
    
    # Email pattern
    EMAIL = re.compile(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    )
    
    # Phone patterns
    PHONE = re.compile(
        r'(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
    )
    
    # URL patterns
    URL = re.compile(
        r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?'
    )
    
    GITHUB_URL = re.compile(
        r'(?:https?://)?(?:www\.)?github\.com/([A-Za-z0-9_.-]+)/?'
    )
    
    LINKEDIN_URL = re.compile(
        r'(?:https?://)?(?:www\.)?linkedin\.com/in/([A-Za-z0-9_.-]+)/?'
    )
    
    # Section headers (case insensitive)
    SECTION_HEADERS = {
        'experience': re.compile(
            r'(?i)^(?:work\s+)?(?:professional\s+)?(?:employment\s+)?experience(?:\s*:)?|work\s+history(?:\s*:)?|employment\s+history(?:\s*:)?|career\s+summary(?:\s*:)?|professional\s+background(?:\s*:)?|work\s+experience(?:\s*:)?|professional\s+experience(?:\s*:)?|relevant\s+experience(?:\s*:)?|career\s+history(?:\s*:)?',
            re.MULTILINE
        ),
        'education': re.compile(
            r'(?i)^education(?:al\s+background)?(?:\s*:)?|academic\s+background(?:\s*:)?|qualifications(?:\s*:)?|academic\s+credentials(?:\s*:)?|academic\s+history(?:\s*:)?',
            re.MULTILINE
        ),
        'skills': re.compile(
            r'(?i)^(?:technical\s+)?skills(?:\s*:)?|competencies(?:\s*:)?|technologies(?:\s*:)?|proficiencies(?:\s*:)?|technical\s+competencies(?:\s*:)?|core\s+skills(?:\s*:)?|key\s+skills(?:\s*:)?|expertise(?:\s*:)?|technical\s+expertise(?:\s*:)?',
            re.MULTILINE
        ),
        'projects': re.compile(
            r'(?i)^projects?(?:\s*:)?|selected\s+projects(?:\s*:)?|key\s+projects(?:\s*:)?|personal\s+projects(?:\s*:)?|professional\s+projects(?:\s*:)?|notable\s+projects(?:\s*:)?',
            re.MULTILINE
        ),
        'certifications': re.compile(
            r'(?i)^certifications?(?:\s*:)?|licenses?(?:\s*:)?|credentials?(?:\s*:)?|professional\s+certifications?(?:\s*:)?|certificates?(?:\s*:)?',
            re.MULTILINE
        ),
        'summary': re.compile(
            r'(?i)^(?:professional\s+)?summary(?:\s*:)?|profile(?:\s*:)?|objective(?:\s*:)?|about\s+me(?:\s*:)?|career\s+objective(?:\s*:)?|professional\s+profile(?:\s*:)?|executive\s+summary(?:\s*:)?|career\s+summary(?:\s*:)?',
            re.MULTILINE
        ),
        'languages': re.compile(
            r'(?i)^languages?(?:\s*:)?|linguistic\s+skills(?:\s*:)?|language\s+proficiency(?:\s*:)?',
            re.MULTILINE
        )
    }
    
    # University/College names pattern
    UNIVERSITY_KEYWORDS = re.compile(
        r'(?i)\b(?:university|college|institute|school|academy|polytechnic)\b'
    )
    
    # Degree patterns
    DEGREE_PATTERNS = re.compile(
        r'(?i)\b(?:bachelor|master|phd|doctorate|associate|diploma|certificate|b\.?s\.?|m\.?s\.?|b\.?a\.?|m\.?a\.?|m\.?b\.?a\.?|b\.?tech|m\.?tech)\b'
    )
    
    # GPA pattern
    GPA_PATTERN = re.compile(
        r'(?i)gpa:?\s*(\d+\.?\d*)\s*(?:/\s*(\d+\.?\d*))?'
    )
    
    # Location patterns (City, State format)
    LOCATION_PATTERN = re.compile(
        r'\b([A-Za-z][A-Za-z\s\-\.]+?),\s*([A-Z]{2})\b'
    )
    
    # Additional location patterns
    LOCATION_PATTERNS = [
        re.compile(r'\b([A-Za-z][A-Za-z\s\-\.]+?),\s*([A-Z]{2})\b'),  # City, ST
        re.compile(r'\b([A-Za-z][A-Za-z\s\-\.]+?),\s*([A-Za-z][A-Za-z\s]+?)(?:,\s*([A-Z]{2}))?\b'),  # City, State
        re.compile(r'\b([A-Za-z][A-Za-z\s\-\.]+?)\s*\|\s*([A-Z]{2})\b'),  # City | ST
        re.compile(r'\b([A-Za-z][A-Za-z\s\-\.]+?)\s*•\s*([A-Z]{2})\b'),  # City • ST
    ]
    
    # Job title indicators
    JOB_TITLE_KEYWORDS = re.compile(
        r'(?i)\b(?:engineer|developer|manager|analyst|specialist|coordinator|director|associate|senior|junior|lead|principal|architect|consultant|intern|designer|administrator|executive|officer|technician|supervisor|assistant|representative|advisor|strategist|scientist|researcher|programmer|tester|writer|editor|trainer|instructor|planner|producer|expert|head|chief|vp|vice\s+president|president|ceo|cto|cfo|coo|founder|co-founder|owner|partner)\b'
    )
    
    # Company indicators
    COMPANY_SUFFIXES = re.compile(
        r'(?i)\b(?:inc|llc|corp|corporation|ltd|limited|co|company|group|technologies|tech|systems|solutions|services|consulting|associates|partners|industries|enterprises|holdings|ventures|labs|laboratory|studios|agency|firm|consultancy|institute|foundation|organization|bank|financial|capital|global|international|worldwide)\b'
    )
    
    # Date patterns
    DATE_PATTERNS = [
        re.compile(r'(?i)(jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|september|oct|october|nov|november|dec|december)[a-z]*\s*,?\s*\d{4}'),
        re.compile(r'\d{1,2}/\d{4}'),
        re.compile(r'\d{1,2}-\d{4}'),
        re.compile(r'\d{4}'),
        re.compile(r'(?i)(spring|summer|fall|autumn|winter)\s+\d{4}'),
        re.compile(r'\d{1,2}/\d{1,2}/\d{2,4}'),
        re.compile(r'\d{1,2}-\d{1,2}-\d{2,4}'),
        re.compile(r'\d{4}\s*-\s*\d{4}'),
        re.compile(r'(?i)(jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|september|oct|october|nov|november|dec|december)[a-z]*\s*\d{1,2}\s*,?\s*\d{4}')
    ]
    
    @classmethod
    def find_section_boundaries(cls, text: str) -> Dict[str, tuple]:
        """
        Find section boundaries in resume text.
        
        Args:
            text: Resume text
            
        Returns:
            Dictionary mapping section names to (start, end) positions
        """
        sections = {}
        text_lines = text.split('\n')
        
        # Track line positions in original text
        line_positions = []
        current_pos = 0
        for line in text_lines:
            line_positions.append(current_pos)
            current_pos += len(line) + 1  # +1 for newline
        line_positions.append(len(text))  # Add end position
        
        # Find all section headers with their positions
        found_sections = []
        
        for i, line in enumerate(text_lines):
            line_stripped = line.strip()
            if not line_stripped:
                continue
                
            # Check if line is a section header
            for section_name, pattern in cls.SECTION_HEADERS.items():
                if pattern.match(line_stripped):
                    # Additional validation: section headers are usually:
                    # 1. In all caps or title case
                    # 2. Short (less than 50 chars)
                    # 3. Often followed by a blank line or different formatting
                    
                    if len(line_stripped) < 50:
                        # Check if next line is blank or has different formatting
                        is_header = False
                        
                        # Check if all caps
                        if line_stripped.isupper():
                            is_header = True
                        # Check if followed by blank line
                        elif i + 1 < len(text_lines) and not text_lines[i + 1].strip():
                            is_header = True
                        # Check if followed by a line with different indentation
                        elif i + 1 < len(text_lines):
                            current_indent = len(line) - len(line.lstrip())
                            next_indent = len(text_lines[i + 1]) - len(text_lines[i + 1].lstrip())
                            if next_indent > current_indent:
                                is_header = True
                        # Check if line ends with colon
                        elif line_stripped.endswith(':'):
                            is_header = True
                        # Default to true for strong matches
                        else:
                            is_header = True
                        
                        if is_header:
                            start_pos = line_positions[i]
                            # Start after the header line
                            content_start = line_positions[i + 1] if i + 1 < len(line_positions) else start_pos
                            found_sections.append((section_name, i, content_start))
                            break
        
        # Remove duplicate sections (keep first occurrence)
        seen_sections = set()
        unique_sections = []
        for section_name, line_num, start_pos in found_sections:
            if section_name not in seen_sections:
                seen_sections.add(section_name)
                unique_sections.append((section_name, line_num, start_pos))
        
        # Sort by line number
        unique_sections.sort(key=lambda x: x[1])
        
        # Calculate end positions
        result = {}
        for i, (section_name, line_num, start_pos) in enumerate(unique_sections):
            # End position is start of next section or end of text
            if i + 1 < len(unique_sections):
                end_pos = unique_sections[i + 1][2]
            else:
                end_pos = len(text)
            
            result[section_name] = (start_pos, end_pos)
        
        return result
    
    @classmethod
    def extract_emails(cls, text: str) -> List[str]:
        """Extract email addresses from text."""
        return cls.EMAIL.findall(text)
    
    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        """Extract URLs from text."""
        return cls.URL.findall(text)
    
    @classmethod
    def extract_github_username(cls, text: str) -> Optional[str]:
        """Extract GitHub username from text."""
        match = cls.GITHUB_URL.search(text)
        return match.group(1) if match else None
    
    @classmethod
    def extract_linkedin_username(cls, text: str) -> Optional[str]:
        """Extract LinkedIn username from text."""
        match = cls.LINKEDIN_URL.search(text)
        return match.group(1) if match else None
    
    @classmethod
    def extract_locations(cls, text: str) -> List[tuple]:
        """Extract locations in 'City, State' format."""
        return cls.LOCATION_PATTERN.findall(text)
    
    @classmethod
    def extract_gpa(cls, text: str) -> Optional[tuple]:
        """
        Extract GPA from text.
        
        Returns:
            Tuple of (gpa, scale) or None if not found
        """
        match = cls.GPA_PATTERN.search(text)
        if match:
            gpa = float(match.group(1))
            scale = float(match.group(2)) if match.group(2) else 4.0
            return (gpa, scale)
        return None
    
    @classmethod
    def is_likely_university(cls, text: str) -> bool:
        """Check if text likely contains a university name."""
        return bool(cls.UNIVERSITY_KEYWORDS.search(text))
    
    @classmethod
    def is_likely_degree(cls, text: str) -> bool:
        """Check if text likely contains a degree."""
        return bool(cls.DEGREE_PATTERNS.search(text))
    
    @classmethod
    def is_likely_job_title(cls, text: str) -> bool:
        """Check if text likely contains a job title."""
        return bool(cls.JOB_TITLE_KEYWORDS.search(text))
    
    @classmethod
    def is_likely_company(cls, text: str) -> bool:
        """Check if text likely contains a company name."""
        return bool(cls.COMPANY_SUFFIXES.search(text))
    
    @classmethod
    def clean_section_text(cls, text: str) -> str:
        """
        Clean text extracted from a section.
        
        Args:
            text: Raw section text
            
        Returns:
            Cleaned text
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove bullet points and common formatting
        text = re.sub(r'^[•▪▫‣⁃]\s*', '', text, flags=re.MULTILINE)
        text = re.sub(r'^[-*]\s*', '', text, flags=re.MULTILINE)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text
    
    @classmethod
    def extract_name_patterns(cls, text: str) -> List[str]:
        """
        Extract potential names using various patterns.
        
        Args:
            text: Text to search for names
            
        Returns:
            List of potential names
        """
        potential_names = []
        
        # Pattern 1: Two or three capitalized words at the beginning
        name_pattern1 = re.compile(r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2})(?:\s|$)', re.MULTILINE)
        matches = name_pattern1.findall(text[:500])  # Look in first 500 chars
        potential_names.extend(matches)
        
        # Pattern 2: Name after common labels
        name_pattern2 = re.compile(r'(?:Name|Contact):\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2})', re.IGNORECASE)
        matches = name_pattern2.findall(text[:500])
        potential_names.extend(matches)
        
        # Pattern 3: All caps name (JOHN DOE)
        name_pattern3 = re.compile(r'^([A-Z]{2,}(?:\s+[A-Z]{2,}){1,2})(?:\s|$)', re.MULTILINE)
        matches = name_pattern3.findall(text[:500])
        potential_names.extend([name.title() for name in matches])
        
        return potential_names
    
    @classmethod
    def is_valid_name(cls, name: str) -> bool:
        """Check if a string is likely a valid person's name."""
        if not name or len(name) < 3 or len(name) > 50:
            return False
        
        # Exclude common resume keywords
        exclude_words = {
            'resume', 'cv', 'curriculum', 'vitae', 'professional', 'profile',
            'summary', 'objective', 'experience', 'education', 'skills',
            'contact', 'information', 'details', 'phone', 'email', 'address'
        }
        
        name_lower = name.lower()
        if any(word in name_lower for word in exclude_words):
            return False
        
        # Check if it has at least one space (first and last name)
        if ' ' not in name.strip():
            return False
        
        # Check if all parts start with capital letters
        parts = name.split()
        if not all(part[0].isupper() for part in parts if part):
            return False
        
        # Check for reasonable number of parts (2-4 typically)
        if len(parts) < 2 or len(parts) > 4:
            return False
        
        return True
    
    @classmethod
    def extract_bullets(cls, text: str) -> List[str]:
        """Extract bullet points from text."""
        bullet_pattern = re.compile(r'^[•▪▫‣⁃\-\*]\s*(.+)$', re.MULTILINE)
        return bullet_pattern.findall(text)
    
    @classmethod
    def normalize_whitespace(cls, text: str) -> str:
        """Normalize whitespace in text."""
        # Replace multiple spaces (but not newlines) with single space
        lines = text.split('\n')
        normalized_lines = []
        for line in lines:
            # Replace multiple spaces within a line with single space
            normalized_line = re.sub(r' +', ' ', line.strip())
            normalized_lines.append(normalized_line)
        
        # Join lines back together
        text = '\n'.join(normalized_lines)
        
        # Replace multiple consecutive blank lines with double newline
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()