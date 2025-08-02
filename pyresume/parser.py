"""
Main ResumeParser class for parsing resumes from various formats.
"""
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path
import re
from datetime import date

from .models.resume import Resume, ContactInfo, Experience, Education, Skill, Project, Certification
from .extractors import pdf, docx, text
from .utils import DateParser, PhoneParser, ResumePatterns


class ResumeParser:
    """
    Main parser class for extracting structured data from resumes.
    
    Supports PDF, DOCX, and plain text formats.
    """
    
    def __init__(self):
        self.extractors = {
            '.pdf': pdf.PDFExtractor(),
            '.docx': docx.DOCXExtractor(),
            '.txt': text.TextExtractor(),
        }
    
    def parse(self, file_path: str) -> Resume:
        """
        Parse a resume file and return structured data.
        
        Args:
            file_path: Path to the resume file
            
        Returns:
            Resume object containing extracted data
            
        Raises:
            ValueError: If file format is not supported
            FileNotFoundError: If file doesn't exist
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        extension = path.suffix.lower()
        
        if extension not in self.extractors:
            supported = ', '.join(self.extractors.keys())
            raise ValueError(f"Unsupported file format: {extension}. Supported: {supported}")
        
        extractor = self.extractors[extension]
        text_content = extractor.extract_text(file_path)
        
        return self._parse_text(text_content)
    
    def parse_text(self, text: str) -> Resume:
        """
        Parse resume from raw text content.
        
        Args:
            text: Raw text content of the resume
            
        Returns:
            Resume object containing extracted data
        """
        return self._parse_text(text)
    
    def _parse_text(self, text: str) -> Resume:
        """
        Internal method to parse text content into structured data.
        
        Args:
            text: Raw text content
            
        Returns:
            Resume object
        """
        # Initialize resume object
        resume = Resume(raw_text=text)
        
        try:
            # Normalize text
            text = ResumePatterns.normalize_whitespace(text)
            
            # Find section boundaries
            sections = ResumePatterns.find_section_boundaries(text)
            
            # Extract contact information (usually at the beginning)
            try:
                contact_info, contact_confidence = self._extract_contact_info(text)
                resume.contact_info = contact_info
                resume.confidence_scores['contact_info'] = contact_confidence
            except Exception as e:
                resume.confidence_scores['contact_info'] = 0.0
                print(f"Error extracting contact info: {e}")
            
            # Extract summary if present
            try:
                if 'summary' in sections:
                    start, end = sections['summary']
                    summary_text = text[start:end].strip()
                    resume.summary = self._clean_section_content(summary_text)
                    resume.confidence_scores['summary'] = 0.9 if resume.summary else 0.0
                else:
                    # Try to find summary in first part of resume
                    first_part = text[:1000]
                    for keyword in ['summary', 'objective', 'profile']:
                        if keyword in first_part.lower():
                            # Extract a few lines after the keyword
                            idx = first_part.lower().find(keyword)
                            summary_candidate = first_part[idx:idx+500].strip()
                            summary_lines = summary_candidate.split('\n')[1:4]
                            if summary_lines:
                                resume.summary = ' '.join(summary_lines).strip()
                                resume.confidence_scores['summary'] = 0.7
                                break
            except Exception as e:
                resume.confidence_scores['summary'] = 0.0
                print(f"Error extracting summary: {e}")
            
            # Extract experience
            try:
                if 'experience' in sections:
                    start, end = sections['experience']
                    experience_text = text[start:end]
                    experience_list, exp_confidence = self._extract_experience(experience_text)
                    resume.experience = experience_list
                    resume.confidence_scores['experience'] = exp_confidence
                else:
                    # Try to find experience in the whole text if section not found
                    experience_list, exp_confidence = self._extract_experience(text)
                    if experience_list:
                        resume.experience = experience_list
                        resume.confidence_scores['experience'] = exp_confidence * 0.7  # Lower confidence
            except Exception as e:
                resume.confidence_scores['experience'] = 0.0
                print(f"Error extracting experience: {e}")
            
            # Extract education
            try:
                if 'education' in sections:
                    start, end = sections['education']
                    education_text = text[start:end]
                    education_list, edu_confidence = self._extract_education(education_text)
                    resume.education = education_list
                    resume.confidence_scores['education'] = edu_confidence
                else:
                    # Try to find education in the whole text if section not found
                    education_list, edu_confidence = self._extract_education(text)
                    if education_list:
                        resume.education = education_list
                        resume.confidence_scores['education'] = edu_confidence * 0.7  # Lower confidence
            except Exception as e:
                resume.confidence_scores['education'] = 0.0
                print(f"Error extracting education: {e}")
            
            # Extract skills
            try:
                if 'skills' in sections:
                    start, end = sections['skills']
                    skills_text = text[start:end]
                    skills_list, skills_confidence = self._extract_skills(skills_text)
                    resume.skills = skills_list
                    resume.confidence_scores['skills'] = skills_confidence
                else:
                    # Extract skills from the entire document
                    skills_list, skills_confidence = self._extract_skills(text)
                    resume.skills = skills_list
                    resume.confidence_scores['skills'] = skills_confidence * 0.8
            except Exception as e:
                resume.confidence_scores['skills'] = 0.0
                print(f"Error extracting skills: {e}")
            
            # Extract projects
            try:
                if 'projects' in sections:
                    start, end = sections['projects']
                    projects_text = text[start:end]
                    projects_list, proj_confidence = self._extract_projects(projects_text)
                    resume.projects = projects_list
                    resume.confidence_scores['projects'] = proj_confidence
            except Exception as e:
                resume.confidence_scores['projects'] = 0.0
                print(f"Error extracting projects: {e}")
            
            # Extract certifications
            try:
                if 'certifications' in sections:
                    start, end = sections['certifications']
                    cert_text = text[start:end]
                    cert_list, cert_confidence = self._extract_certifications(cert_text)
                    resume.certifications = cert_list
                    resume.confidence_scores['certifications'] = cert_confidence
                else:
                    # Try to find certifications in whole text
                    cert_list, cert_confidence = self._extract_certifications(text)
                    if cert_list:
                        resume.certifications = cert_list
                        resume.confidence_scores['certifications'] = cert_confidence * 0.7
            except Exception as e:
                resume.confidence_scores['certifications'] = 0.0
                print(f"Error extracting certifications: {e}")
            
            # Extract languages
            try:
                if 'languages' in sections:
                    start, end = sections['languages']
                    lang_text = text[start:end]
                    languages = self._extract_languages(lang_text)
                    resume.languages = languages
                    resume.confidence_scores['languages'] = 0.9 if languages else 0.0
            except Exception as e:
                resume.confidence_scores['languages'] = 0.0
                print(f"Error extracting languages: {e}")
            
            # Calculate overall confidence
            confidence_values = [v for v in resume.confidence_scores.values() if v > 0]
            overall_confidence = sum(confidence_values) / len(confidence_values) if confidence_values else 0.0
            
            # Store extraction metadata
            resume.extraction_metadata = {
                'sections_found': list(sections.keys()),
                'text_length': len(text),
                'lines_count': len(text.split('\n')),
                'has_email': bool(resume.contact_info.email),
                'has_phone': bool(resume.contact_info.phone),
                'has_name': bool(resume.contact_info.name),
                'experience_count': len(resume.experience),
                'education_count': len(resume.education),
                'skills_count': len(resume.skills),
                'projects_count': len(resume.projects),
                'certifications_count': len(resume.certifications),
                'overall_confidence': round(overall_confidence, 2)
            }
            
        except Exception as e:
            print(f"Error in resume parsing: {e}")
            # Ensure we return a valid Resume object even on error
            resume.extraction_metadata = {
                'error': str(e),
                'sections_found': [],
                'text_length': len(text),
                'overall_confidence': 0.0
            }
        
        return resume
    
    def _extract_contact_info(self, text: str) -> Tuple[ContactInfo, float]:
        """
        Extract contact information from resume text.
        
        Args:
            text: Resume text
            
        Returns:
            Tuple of (ContactInfo, confidence_score)
        """
        contact = ContactInfo()
        confidence_scores = []
        
        # Extract name (usually at the beginning, in first 5 lines)
        lines = text.split('\n')[:10]
        name = self._extract_name(lines)
        if name:
            # Clean up name - sometimes it includes extra lines
            name_cleaned = name.strip()
            if '\n' in name_cleaned:
                name_cleaned = name_cleaned.split('\n')[0].strip()
            contact.name = name_cleaned
            confidence_scores.append(0.9)
        else:
            confidence_scores.append(0.3)
        
        # Extract email
        emails = ResumePatterns.extract_emails(text)
        if emails:
            contact.email = emails[0]  # Take the first email
            confidence_scores.append(1.0)  # Email regex is very reliable
        else:
            confidence_scores.append(0.0)
        
        # Extract phone
        phones = PhoneParser.extract_phone_numbers(text)
        if phones:
            # Validate and format the first phone number
            for phone in phones:
                if PhoneParser.validate_phone_number(phone):
                    contact.phone = PhoneParser.format_phone_number(phone)
                    confidence_scores.append(0.95)
                    break
            else:
                contact.phone = phones[0]  # Use first even if not validated
                confidence_scores.append(0.7)
        else:
            confidence_scores.append(0.0)
        
        # Extract LinkedIn
        linkedin_username = ResumePatterns.extract_linkedin_username(text)
        if linkedin_username:
            contact.linkedin = f"https://linkedin.com/in/{linkedin_username}"
            confidence_scores.append(0.95)
        else:
            # Look for LinkedIn URL without username extraction
            if 'linkedin.com' in text.lower():
                urls = ResumePatterns.extract_urls(text)
                for url in urls:
                    if 'linkedin.com' in url.lower():
                        contact.linkedin = url
                        confidence_scores.append(0.8)
                        break
        
        # Extract GitHub
        github_username = ResumePatterns.extract_github_username(text)
        if github_username:
            contact.github = f"https://github.com/{github_username}"
            confidence_scores.append(0.95)
        else:
            # Look for GitHub URL without username extraction
            if 'github.com' in text.lower():
                urls = ResumePatterns.extract_urls(text)
                for url in urls:
                    if 'github.com' in url.lower():
                        contact.github = url
                        confidence_scores.append(0.8)
                        break
        
        # Extract location/address
        locations = ResumePatterns.extract_locations(text[:1000])  # Look in first part
        if locations:
            city, state = locations[0]
            contact.address = f"{city}, {state}"
            confidence_scores.append(0.8)
        
        # Extract website (other than LinkedIn/GitHub)
        urls = ResumePatterns.extract_urls(text)
        for url in urls:
            if 'linkedin.com' not in url.lower() and 'github.com' not in url.lower():
                contact.website = url
                confidence_scores.append(0.7)
                break
        
        # Calculate overall confidence
        overall_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
        
        return contact, overall_confidence
    
    def _extract_name(self, lines: List[str]) -> Optional[str]:
        """
        Extract name from the beginning lines of resume.
        
        Args:
            lines: First few lines of resume
            
        Returns:
            Extracted name or None
        """
        # Try pattern-based extraction first
        text_start = '\n'.join(lines[:10])
        potential_names = ResumePatterns.extract_name_patterns(text_start)
        
        # Validate and return the first valid name
        for name in potential_names:
            if ResumePatterns.is_valid_name(name):
                return name
        
        # Fallback: Look for name in first few non-empty lines
        for i, line in enumerate(lines):
            line = line.strip()
            if not line or i > 5:  # Only check first 5 non-empty lines
                continue
            
            # Skip lines that look like headers or contain special characters
            if any(char in line for char in ['@', '|', '•', '/', 'http', 'www', ':', '-', '(', ')']):
                continue
            
            # Skip lines with numbers (likely phone)
            if re.search(r'\d{3,}', line):
                continue
            
            # Skip lines that are too short or too long
            if len(line) < 5 or len(line) > 50:
                continue
            
            # Check if line contains name-like pattern
            words = line.split()
            if 2 <= len(words) <= 4:
                # Check if words start with capital letters or are all caps
                if all(word[0].isupper() or word.isupper() for word in words if word and word.isalpha()):
                    # Additional validation
                    if ResumePatterns.is_valid_name(line):
                        # Don't include lines that have job title keywords
                        if not ResumePatterns.is_likely_job_title(line):
                            return line.title() if line.isupper() else line
        
        return None
    
    def _extract_experience(self, text: str) -> Tuple[List[Experience], float]:
        """
        Extract work experience from text.
        
        Args:
            text: Experience section text
            
        Returns:
            Tuple of (list of Experience objects, confidence_score)
        """
        experiences = []
        confidence_scores = []
        
        # Split into potential experience blocks
        blocks = self._split_into_blocks(text)
        
        for block in blocks:
            exp = self._parse_experience_block(block)
            if exp and (exp.title or exp.company):
                experiences.append(exp)
                # Calculate confidence for this experience
                score = 0.0
                if exp.title:
                    score += 0.3
                if exp.company:
                    score += 0.3
                if exp.start_date:
                    score += 0.2
                if exp.description or exp.responsibilities:
                    score += 0.2
                confidence_scores.append(score)
        
        # Calculate overall confidence
        overall_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
        
        return experiences, overall_confidence
    
    def _parse_experience_block(self, block: str) -> Optional[Experience]:
        """
        Parse a single experience block.
        
        Args:
            block: Text block potentially containing experience
            
        Returns:
            Experience object or None
        """
        lines = block.strip().split('\n')
        if not lines:
            return None
        
        exp = Experience()
        
        # Track which lines we've used
        used_lines = set()
        
        # Look for dates first (they help identify the structure)
        for i, line in enumerate(lines[:4]):  # Check first 4 lines
            if any(pattern.search(line) for pattern in ResumePatterns.DATE_PATTERNS):
                start_date, end_date = DateParser.extract_date_range(line)
                if start_date:
                    exp.start_date = start_date
                    exp.end_date = end_date
                    if DateParser.is_current_position(line):
                        exp.current = True
                        exp.end_date = None
                    used_lines.add(i)
                break
        
        # Parse title and company based on common patterns
        title_found = False
        company_found = False
        
        # Pattern 1: Title at Company (Location)
        for i, line in enumerate(lines[:3]):
            if i in used_lines:
                continue
                
            match = re.match(r'^(.+?)\s+(?:at|@)\s+(.+?)(?:\s*[\|\,]\s*(.+))?$', line, re.IGNORECASE)
            if match:
                exp.title = match.group(1).strip()
                exp.company = match.group(2).strip()
                if match.group(3):
                    location_part = match.group(3).strip()
                    # Check if it's a location
                    if re.search(r'\b[A-Z]{2}\b', location_part):
                        exp.location = location_part
                title_found = company_found = True
                used_lines.add(i)
                break
        
        # Pattern 2: Company | Title or Title | Company
        if not (title_found and company_found):
            for i, line in enumerate(lines[:3]):
                if i in used_lines:
                    continue
                    
                if '|' in line or '•' in line or ' - ' in line:
                    separators = ['|', '•', ' - ']
                    for sep in separators:
                        if sep in line:
                            parts = line.split(sep)
                            if len(parts) >= 2:
                                part1 = parts[0].strip()
                                part2 = parts[1].strip()
                                
                                # Determine which is title and which is company
                                if ResumePatterns.is_likely_job_title(part1):
                                    exp.title = part1
                                    exp.company = part2
                                elif ResumePatterns.is_likely_company(part2):
                                    exp.title = part1
                                    exp.company = part2
                                elif ResumePatterns.is_likely_job_title(part2):
                                    exp.company = part1
                                    exp.title = part2
                                else:
                                    # Default assumption
                                    exp.title = part1
                                    exp.company = part2
                                
                                title_found = company_found = True
                                used_lines.add(i)
                                break
                    if title_found:
                        break
        
        # Pattern 3: Title and company on separate lines
        if not title_found or not company_found:
            for i, line in enumerate(lines[:3]):
                if i in used_lines:
                    continue
                    
                line = line.strip()
                if not title_found and ResumePatterns.is_likely_job_title(line):
                    exp.title = line
                    title_found = True
                    used_lines.add(i)
                elif not company_found and ResumePatterns.is_likely_company(line):
                    exp.company = line
                    company_found = True
                    used_lines.add(i)
        
        # Extract location if not already found
        if not exp.location:
            # Look in the same line as company or in next few lines
            for i, line in enumerate(lines[:4]):
                if i in used_lines:
                    continue
                    
                # Try different location patterns
                for loc_pattern in ResumePatterns.LOCATION_PATTERNS:
                    match = loc_pattern.search(line)
                    if match:
                        if len(match.groups()) >= 2:
                            city = match.group(1).strip()
                            state = match.group(2).strip()
                            exp.location = f"{city}, {state}"
                            used_lines.add(i)
                            break
                
                # Also check if location is in the same line as dates
                if not exp.location and exp.start_date and i < len(lines):
                    # Remove date part and check for location
                    line_without_date = re.sub(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}.*', '', line, flags=re.IGNORECASE)
                    line_without_date = re.sub(r'\d{4}\s*[-–]\s*(?:\d{4}|Present|Current).*', '', line_without_date)
                    
                    for loc_pattern in ResumePatterns.LOCATION_PATTERNS:
                        match = loc_pattern.search(line_without_date)
                        if match:
                            if len(match.groups()) >= 2:
                                city = match.group(1).strip()
                                state = match.group(2).strip()
                                exp.location = f"{city}, {state}"
                                break
                
                if exp.location:
                    break
        
        # Extract description and responsibilities
        desc_lines = []
        resp_lines = []
        
        for i, line in enumerate(lines):
            if i in used_lines:
                continue
                
            line = line.strip()
            if not line:
                continue
            
            # Skip lines that look like headers
            if re.match(r'^[A-Z][A-Z\s]+:?$', line) and len(line) < 30:
                continue
            
            # Lines starting with bullets are responsibilities
            bullet_match = re.match(r'^[•▪▫‣⁃\-\*]\s*(.+)', line)
            if bullet_match:
                resp_lines.append(bullet_match.group(1))
            else:
                # Check if line starts with action verb (common in responsibilities)
                action_verbs = ['managed', 'developed', 'led', 'created', 'implemented',
                               'designed', 'built', 'established', 'improved', 'coordinated',
                               'analyzed', 'increased', 'reduced', 'streamlined', 'optimized']
                if any(line.lower().startswith(verb) for verb in action_verbs):
                    resp_lines.append(line)
                else:
                    # Other lines are description
                    desc_lines.append(line)
        
        if desc_lines:
            exp.description = ' '.join(desc_lines[:3])  # Limit description length
        if resp_lines:
            exp.responsibilities = resp_lines
        
        # Only return if we found at least title or company
        if exp.title or exp.company:
            return exp
        return None
    
    def _extract_education(self, text: str) -> Tuple[List[Education], float]:
        """
        Extract education information from text.
        
        Args:
            text: Education section text
            
        Returns:
            Tuple of (list of Education objects, confidence_score)
        """
        educations = []
        confidence_scores = []
        
        # Split into potential education blocks
        blocks = self._split_into_blocks(text)
        
        for block in blocks:
            edu = self._parse_education_block(block)
            if edu and (edu.institution or edu.degree):
                educations.append(edu)
                # Calculate confidence for this education
                score = 0.0
                if edu.institution:
                    score += 0.4
                if edu.degree:
                    score += 0.4
                if edu.graduation_date:
                    score += 0.1
                if edu.gpa:
                    score += 0.1
                confidence_scores.append(score)
        
        # Calculate overall confidence
        overall_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
        
        return educations, overall_confidence
    
    def _parse_education_block(self, block: str) -> Optional[Education]:
        """
        Parse a single education block.
        
        Args:
            block: Text block potentially containing education
            
        Returns:
            Education object or None
        """
        lines = block.strip().split('\n')
        if not lines:
            return None
        
        edu = Education()
        used_lines = set()
        
        # Common degree patterns
        degree_patterns = [
            # Bachelor of Science in Computer Science
            r'(?i)(bachelor|master|phd|ph\.d\.|doctorate|associate|diploma)(?:\'s)?(?:\s+of)?\s+(?:of\s+)?(science|arts|engineering|business|technology|philosophy|education|fine\s+arts|laws?)\s*(?:in\s+)?([A-Za-z\s,]+?)(?:\s*[\|\,\.]|$)',
            # B.S. Computer Science, M.S. Data Science
            r'(?i)(b\.?s\.?|m\.?s\.?|b\.?a\.?|m\.?a\.?|b\.?tech|m\.?tech|m\.?b\.?a\.?|j\.?d\.?|m\.?d\.?|ph\.?d\.?)\s*(?:in\s+)?([A-Za-z\s,]+?)(?:\s*[\|\,\.]|$)',
            # Computer Science, Bachelor of Science
            r'(?i)([A-Za-z\s]+?),\s*(bachelor|master|phd|doctorate|associate)(?:\'s)?(?:\s+of)?\s+(science|arts|engineering|business|technology)',
            # Simple degree mentions
            r'(?i)(bachelor|master|phd|doctorate|associate|diploma|certificate)(?:\'s)?(?:\s+degree)?'
        ]
        
        # Parse degree and major
        degree_found = False
        for i, line in enumerate(lines):
            if degree_found:
                break
                
            for pattern in degree_patterns:
                match = re.search(pattern, line)
                if match:
                    groups = match.groups()
                    if len(groups) >= 3:
                        # Pattern with degree type, field, and major
                        degree_type = groups[0]
                        field = groups[1] if len(groups) > 1 else ''
                        major = groups[2] if len(groups) > 2 else ''
                        edu.degree = f"{degree_type} of {field}".strip().title()
                        if major:
                            edu.major = major.strip().title()
                    elif len(groups) >= 2:
                        # Pattern with degree abbreviation and major
                        edu.degree = groups[0].upper().replace('.', '.')
                        edu.major = groups[1].strip().title()
                    else:
                        # Simple degree
                        edu.degree = match.group(0).strip().title()
                    
                    degree_found = True
                    used_lines.add(i)
                    break
        
        # Look for university/institution
        for i, line in enumerate(lines):
            if i in used_lines:
                continue
                
            # Skip if it's just a location
            if re.match(r'^[A-Za-z\s]+,\s*[A-Z]{2}$', line.strip()):
                continue
                
            if ResumePatterns.is_likely_university(line):
                edu.institution = line.strip()
                used_lines.add(i)
                break
        
        # If no institution found, check first few lines
        if not edu.institution:
            for i, line in enumerate(lines[:3]):
                if i in used_lines:
                    continue
                    
                # Look for capitalized multi-word phrases
                if len(line.split()) >= 2 and not re.search(r'\d{4}', line):
                    # Exclude common non-institution words
                    exclude = ['expected', 'graduation', 'gpa', 'major', 'minor', 'concentration']
                    if not any(word in line.lower() for word in exclude):
                        edu.institution = line.strip()
                        used_lines.add(i)
                        break
        
        # Extract GPA with more patterns
        gpa_patterns = [
            r'(?i)gpa:?\s*(\d+\.?\d*)\s*(?:/\s*(\d+\.?\d*))?',
            r'(?i)grade\s*point\s*average:?\s*(\d+\.?\d*)\s*(?:/\s*(\d+\.?\d*))?',
            r'(?i)cumulative\s*gpa:?\s*(\d+\.?\d*)\s*(?:/\s*(\d+\.?\d*))?',
            r'(\d+\.\d{1,2})\s*/\s*(\d+\.\d{1,2})',  # 3.85/4.00
        ]
        
        for pattern in gpa_patterns:
            match = re.search(pattern, ' '.join(lines))
            if match:
                gpa = float(match.group(1))
                scale = float(match.group(2)) if match.group(2) else 4.0
                edu.gpa = f"{gpa}/{scale}"
                break
        
        # Extract dates - look for graduation date
        date_candidates = []
        for i, line in enumerate(lines):
            # Look for explicit graduation dates
            if re.search(r'(?i)graduat', line):
                # Extract date from the graduation line
                for pattern in ResumePatterns.DATE_PATTERNS:
                    match = pattern.search(line)
                    if match:
                        parsed_date = DateParser.parse_date(match.group(0))
                        if parsed_date:
                            edu.graduation_date = parsed_date
                            break
                if edu.graduation_date:
                    break
            
            # Collect all dates as candidates
            for pattern in ResumePatterns.DATE_PATTERNS:
                matches = pattern.findall(line)
                for match in matches:
                    parsed_date = DateParser.parse_date(str(match))
                    if parsed_date:
                        date_candidates.append(parsed_date)
        
        # If no explicit graduation date, use the most reasonable date found
        if not edu.graduation_date and date_candidates:
            # Filter out future dates (likely not graduation dates)
            past_dates = [d for d in date_candidates if d <= date.today()]
            if past_dates:
                edu.graduation_date = max(past_dates)
        
        # Extract location
        for i, line in enumerate(lines):
            if i in used_lines:
                continue
                
            for loc_pattern in ResumePatterns.LOCATION_PATTERNS:
                match = loc_pattern.search(line)
                if match:
                    if len(match.groups()) >= 2:
                        city = match.group(1).strip()
                        state = match.group(2).strip()
                        edu.location = f"{city}, {state}"
                        break
            if edu.location:
                break
        
        # Extract honors/minor if present
        honors_patterns = [
            r'(?i)magna\s+cum\s+laude|summa\s+cum\s+laude|cum\s+laude',
            r'(?i)dean\'s\s+list',
            r'(?i)honors|with\s+honors',
        ]
        
        minor_patterns = [
            r'(?i)minor:?\s*(?:in\s+)?([A-Za-z\s]+?)(?:\s*[\|\,\.]|$)',
            r'(?i)with\s+(?:a\s+)?minor\s+in\s+([A-Za-z\s]+?)(?:\s*[\|\,\.]|$)',
        ]
        
        for line in lines:
            # Check for honors
            for pattern in honors_patterns:
                if re.search(pattern, line):
                    if edu.degree:
                        edu.degree += f" ({re.search(pattern, line).group(0).title()})"
                    break
            
            # Check for minor
            for pattern in minor_patterns:
                match = re.search(pattern, line)
                if match:
                    edu.minor = match.group(1).strip().title()
                    break
        
        # Only return if we found institution or degree
        if edu.institution or edu.degree:
            return edu
        return None
    
    def _extract_skills(self, text: str) -> Tuple[List[Skill], float]:
        """
        Extract skills from text.
        
        Args:
            text: Skills section text or full resume text
            
        Returns:
            Tuple of (list of Skill objects, confidence_score)
        """
        skills = []
        skill_names = set()
        
        # Common skill categories
        categories = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'go', 'rust', 'php', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'typescript', 'perl', 'bash', 'shell', 'powershell', 'vba', 'objective-c', 'dart', 'lua', 'groovy', 'haskell', 'erlang', 'clojure', 'f#', 'julia', 'fortran', 'cobol', 'pascal', 'delphi'],
            'web': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring', 'rails', 'asp.net', 'jquery', 'bootstrap', 'sass', 'less', 'webpack', 'babel', 'gulp', 'grunt', 'next.js', 'nuxt.js', 'gatsby', 'svelte', 'ember', 'backbone', 'meteor', 'laravel', 'symfony', 'codeigniter', 'fastapi', 'graphql', 'rest', 'soap', 'websocket'],
            'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sqlite', 'cassandra', 'dynamodb', 'elasticsearch', 'neo4j', 'couchdb', 'firebase', 'firestore', 'mariadb', 'db2', 'sybase', 'teradata', 'snowflake', 'redshift', 'bigquery', 'cosmos db', 'memcached', 'influxdb'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'ansible', 'jenkins', 'circleci', 'gitlab', 'github actions', 'travis ci', 'bamboo', 'teamcity', 'puppet', 'chef', 'saltstack', 'vagrant', 'packer', 'consul', 'vault', 'nomad', 'istio', 'helm', 'prometheus', 'grafana', 'datadog', 'new relic', 'cloudformation', 'openstack', 'vmware', 'heroku', 'netlify', 'vercel'],
            'data': ['pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras', 'spark', 'hadoop', 'tableau', 'powerbi', 'looker', 'qlik', 'sas', 'spss', 'stata', 'jupyter', 'matplotlib', 'seaborn', 'plotly', 'bokeh', 'nltk', 'spacy', 'opencv', 'pillow', 'scrapy', 'beautifulsoup', 'selenium', 'airflow', 'luigi', 'dask', 'ray', 'mlflow', 'kubeflow', 'h2o', 'xgboost', 'lightgbm', 'catboost'],
            'tools': ['git', 'jira', 'confluence', 'slack', 'trello', 'asana', 'figma', 'sketch', 'photoshop', 'illustrator', 'xd', 'invision', 'zeplin', 'notion', 'monday', 'basecamp', 'clickup', 'linear', 'shortcut', 'pivotal tracker', 'bugzilla', 'mantis', 'redmine', 'youtrack', 'bitbucket', 'subversion', 'mercurial', 'perforce', 'visual studio', 'vscode', 'intellij', 'eclipse', 'atom', 'sublime', 'vim', 'emacs', 'postman', 'insomnia', 'charles', 'fiddler', 'wireshark']
        }
        
        # Convert text to lowercase for matching
        text_lower = text.lower()
        
        # Extract skills by category
        for category, skill_list in categories.items():
            for skill in skill_list:
                # Use word boundaries for accurate matching
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, text_lower):
                    if skill not in skill_names:
                        skills.append(Skill(name=skill.title(), category=category))
                        skill_names.add(skill)
        
        # Extract skills from bullet points or comma-separated lists
        skill_patterns = [
            r'[•▪▫‣⁃\-\*]\s*([A-Za-z][A-Za-z\s\+\#\.\-/]+?)(?:\s*[\n,;]|$)',
            r'(?:Skills|Technologies|Tools|Proficiencies|Stack|Expertise):\s*([A-Za-z][A-Za-z\s,\+\#\.\-/]+)',
            r'(?:Programming Languages?|Languages?):\s*([A-Za-z][A-Za-z\s,\+\#\.\-/]+)',
            r'(?:Frameworks?|Libraries?):\s*([A-Za-z][A-Za-z\s,\+\#\.\-/]+)',
            r'(?:Databases?|Data Stores?):\s*([A-Za-z][A-Za-z\s,\+\#\.\-/]+)',
            r'(?:Cloud|DevOps|Infrastructure):\s*([A-Za-z][A-Za-z\s,\+\#\.\-/]+)',
        ]
        
        for pattern in skill_patterns:
            matches = re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE)
            for match in matches:
                skill_text = match.group(1)
                # Split by various separators
                potential_skills = re.split(r'[,;/\|]|\s{2,}|\sand\s', skill_text)
                for ps in potential_skills:
                    ps = ps.strip()
                    # Clean up the skill name
                    ps = re.sub(r'\s+', ' ', ps)  # Normalize whitespace
                    ps = ps.rstrip('.')  # Remove trailing period
                    
                    # Validate skill
                    if (ps and 
                        2 <= len(ps) <= 40 and 
                        ps.lower() not in skill_names and
                        not ps.lower().startswith(('with', 'using', 'including', 'such as', 'like', 'for'))):
                        
                        # Try to categorize the skill
                        skill_category = None
                        skill_lower = ps.lower()
                        
                        for category, skill_list in categories.items():
                            if any(s in skill_lower for s in skill_list):
                                skill_category = category
                                break
                        
                        skills.append(Skill(name=ps, category=skill_category))
                        skill_names.add(ps.lower())
        
        # Calculate confidence based on number of skills found
        confidence = min(0.95, len(skills) * 0.05) if skills else 0.0
        
        return skills, confidence
    
    def _extract_projects(self, text: str) -> Tuple[List[Project], float]:
        """
        Extract projects from text.
        
        Args:
            text: Projects section text
            
        Returns:
            Tuple of (list of Project objects, confidence_score)
        """
        projects = []
        blocks = self._split_into_blocks(text)
        
        for block in blocks:
            lines = block.strip().split('\n')
            if not lines:
                continue
            
            project = Project()
            
            # First line is usually project name
            project.name = lines[0].strip()
            
            # Look for URLs
            urls = ResumePatterns.extract_urls(block)
            if urls:
                project.url = urls[0]
            
            # Extract dates
            date_text = ' '.join(lines[:2])
            start_date, end_date = DateParser.extract_date_range(date_text)
            if start_date:
                project.start_date = start_date
                project.end_date = end_date
            
            # Rest is description
            desc_lines = []
            for line in lines[1:]:
                line = line.strip()
                if line and not DateParser.parse_date(line):
                    desc_lines.append(line)
            
            if desc_lines:
                project.description = ' '.join(desc_lines)
            
            # Extract technologies mentioned
            tech_keywords = ['using', 'built with', 'technologies:', 'tech stack:', 'tools:']
            for line in lines:
                line_lower = line.lower()
                for keyword in tech_keywords:
                    if keyword in line_lower:
                        # Extract everything after the keyword
                        idx = line_lower.find(keyword)
                        tech_text = line[idx + len(keyword):].strip()
                        # Split by common separators
                        techs = re.split(r'[,;]', tech_text)
                        project.technologies = [t.strip() for t in techs if t.strip()]
                        break
            
            if project.name:
                projects.append(project)
        
        confidence = 0.8 if projects else 0.0
        return projects, confidence
    
    def _extract_certifications(self, text: str) -> Tuple[List[Certification], float]:
        """
        Extract certifications from text.
        
        Args:
            text: Certifications section text
            
        Returns:
            Tuple of (list of Certification objects, confidence_score)
        """
        certifications = []
        blocks = self._split_into_blocks(text)
        
        for block in blocks:
            lines = block.strip().split('\n')
            if not lines:
                continue
            
            cert = Certification()
            
            # First line is usually certification name
            cert.name = lines[0].strip()
            
            # Look for issuer (common patterns)
            issuer_patterns = [
                r'(?:by|from|issued by|Issuer):\s*([A-Za-z\s\.]+?)(?:\s*[,\.\|]|$)',
                r'(?:by|from|issued by)\s+([A-Za-z\s\.]+?)(?:\s*[,\.\|]|$)',
            ]
            
            for i, line in enumerate(lines):
                for pattern in issuer_patterns:
                    match = re.search(pattern, line, re.IGNORECASE)
                    if match:
                        cert.issuer = match.group(1).strip()
                        break
                
                # Also check if the line after the cert name might be the issuer
                if not cert.issuer and i == 1 and not any(char in line for char in [':', '|', 'Date', 'ID']):
                    # This might be the issuer organization
                    if len(line.split()) >= 2:
                        cert.issuer = line.strip()
                        break
                
                if cert.issuer:
                    break
            
            # Extract dates
            for i, line in enumerate(lines):
                # Look for explicit date labels
                if re.search(r'(?i)(?:Date|Issued|Valid):', line):
                    # Extract date from this line
                    for pattern in ResumePatterns.DATE_PATTERNS:
                        match = pattern.search(line)
                        if match:
                            parsed_date = DateParser.parse_date(match.group(0))
                            if parsed_date and not cert.issue_date:
                                cert.issue_date = parsed_date
                                break
                
                # Look for expiry date
                if re.search(r'(?i)(?:Expir|Valid until):', line):
                    for pattern in ResumePatterns.DATE_PATTERNS:
                        match = pattern.search(line)
                        if match:
                            parsed_date = DateParser.parse_date(match.group(0))
                            if parsed_date:
                                cert.expiry_date = parsed_date
                                break
            
            # Look for credential ID
            id_patterns = [
                r'(?:ID|Credential|Certificate)(?:\s*#)?:\s*([A-Za-z0-9\-]+)',
                r'#\s*([A-Za-z0-9\-]+)',
            ]
            
            for line in lines:
                for pattern in id_patterns:
                    match = re.search(pattern, line, re.IGNORECASE)
                    if match:
                        cert.credential_id = match.group(1).strip()
                        break
                if cert.credential_id:
                    break
            
            if cert.name:
                certifications.append(cert)
        
        confidence = 0.85 if certifications else 0.0
        return certifications, confidence
    
    def _extract_languages(self, text: str) -> List[str]:
        """
        Extract languages from text.
        
        Args:
            text: Languages section text
            
        Returns:
            List of languages
        """
        languages = []
        
        # Common language names
        common_languages = [
            'english', 'spanish', 'french', 'german', 'italian', 'portuguese',
            'russian', 'chinese', 'japanese', 'korean', 'arabic', 'hindi',
            'dutch', 'swedish', 'polish', 'turkish', 'greek', 'hebrew',
            'mandarin', 'cantonese', 'punjabi', 'bengali', 'urdu'
        ]
        
        text_lower = text.lower()
        
        # Look for languages in the text
        for lang in common_languages:
            if lang in text_lower:
                # Capitalize properly
                languages.append(lang.title())
        
        # Also look for patterns like "Native: English"
        pattern = r'(?:Native|Fluent|Proficient|Basic|Intermediate|Advanced|Conversational)(?:\s*:)?\s*([A-Za-z]+)'
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            lang = match.group(1).strip().title()
            if lang not in languages:
                languages.append(lang)
        
        return languages
    
    def _split_into_blocks(self, text: str) -> List[str]:
        """
        Split text into logical blocks (usually separated by blank lines or bullets).
        
        Args:
            text: Text to split
            
        Returns:
            List of text blocks
        """
        # First normalize the text
        text = ResumePatterns.normalize_whitespace(text)
        
        # Split by double newlines first (major blocks)
        major_blocks = re.split(r'\n\s*\n', text)
        
        final_blocks = []
        for block in major_blocks:
            lines = block.split('\n')
            
            # Check if this block looks like an experience/education entry
            # These typically have a title/company on first lines followed by bullets
            has_bullets = any(re.match(r'^[•▪▫‣⁃\-\*]\s', line) for line in lines)
            
            if has_bullets and len(lines) > 3:
                # This looks like a structured entry (experience, education, etc.)
                # Keep it as one block
                final_blocks.append(block)
            else:
                # Split further by patterns
                current_block = []
                
                for i, line in enumerate(lines):
                    # Check if this line starts a new item
                    is_new_item = False
                    
                    if i > 0:  # Don't split on first line
                        # Check various patterns that indicate a new item
                        is_new_item = (
                            # Job title pattern: Title at Company
                            re.search(r'\bat\b.*(?:Inc|LLC|Corp|Company)', line, re.IGNORECASE) or
                            # Date range at the beginning or end of line
                            (re.match(r'^\d{4}', line) or re.search(r'\d{4}\s*[-–]\s*(?:\d{4}|Present|Current)', line)) or
                            # Line is all caps (section header)
                            (line.isupper() and len(line.split()) < 5) or
                            # Common section starters
                            (len(line) > 0 and i > 0 and 
                             ResumePatterns.is_likely_job_title(line) and 
                             not re.match(r'^[•▪▫‣⁃\-\*]', lines[i-1]))
                        )
                    
                    if is_new_item and current_block:
                        # Save current block and start new one
                        final_blocks.append('\n'.join(current_block))
                        current_block = [line]
                    else:
                        current_block.append(line)
                
                if current_block:
                    final_blocks.append('\n'.join(current_block))
        
        return [b.strip() for b in final_blocks if b.strip()]
    
    def _clean_section_content(self, text: str) -> str:
        """
        Clean section content by removing headers and excessive formatting.
        
        Args:
            text: Section text
            
        Returns:
            Cleaned text
        """
        lines = text.split('\n')
        cleaned_lines = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Skip the header line (first line if it matches section pattern)
            if i == 0:
                for pattern in ResumePatterns.SECTION_HEADERS.values():
                    if pattern.match(line):
                        continue
            
            # Remove bullet points
            line = re.sub(r'^[•▪▫‣⁃\-\*]\s*', '', line)
            
            if line:
                cleaned_lines.append(line)
        
        return ' '.join(cleaned_lines)