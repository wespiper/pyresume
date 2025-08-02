#!/usr/bin/env python3
"""
Test script for the pyresume parser.
"""
import sys
sys.path.insert(0, '/Users/wnp/Desktop/pyresume')

from pyresume.parser import ResumeParser
import json

# Test resume text
test_resume = """John Doe
Software Engineer | San Francisco, CA
johndoe@email.com | (555) 123-4567 | linkedin.com/in/johndoe | github.com/johndoe

PROFESSIONAL SUMMARY
Experienced software engineer with 5+ years developing scalable web applications and distributed systems. 
Strong expertise in Python, JavaScript, and cloud technologies. Passionate about building efficient, 
user-friendly solutions that drive business value.

WORK EXPERIENCE

Senior Software Engineer at TechCorp Inc.
San Francisco, CA | June 2020 - Present
• Led development of microservices architecture serving 1M+ daily users
• Implemented CI/CD pipeline reducing deployment time by 60%
• Mentored junior developers and conducted code reviews
• Technologies: Python, Django, Docker, Kubernetes, AWS

Software Engineer - DataSystems LLC
Mountain View, CA | Jan 2018 - May 2020
- Developed RESTful APIs for data processing platform
- Optimized database queries improving performance by 40%
- Built React components for customer-facing dashboard
- Collaborated with cross-functional teams in Agile environment

Junior Developer at StartupXYZ
Palo Alto, CA | July 2016 - December 2017
• Created automated testing framework increasing code coverage to 85%
• Maintained and enhanced legacy PHP applications
• Participated in daily standups and sprint planning

EDUCATION

Bachelor of Science in Computer Science
Stanford University, Stanford, CA
Graduated: June 2016
GPA: 3.8/4.0

SKILLS
Programming Languages: Python, JavaScript, TypeScript, Java, Go
Frameworks: Django, Flask, React, Node.js, Express, Spring Boot
Databases: PostgreSQL, MySQL, MongoDB, Redis
Cloud & DevOps: AWS, Docker, Kubernetes, Jenkins, Terraform
Tools: Git, JIRA, Confluence, VS Code, IntelliJ IDEA

PROJECTS

E-commerce Platform (2021)
Built a scalable e-commerce platform using microservices architecture
Technologies: Python, React, PostgreSQL, Redis, Docker
URL: github.com/johndoe/ecommerce-platform

Data Analytics Dashboard (2020)
Developed real-time analytics dashboard for business intelligence
Technologies: Python, D3.js, MongoDB, WebSocket

CERTIFICATIONS
AWS Certified Solutions Architect - Associate
Issued by: Amazon Web Services
Date: March 2021
Credential ID: AWS-SA-2021-JD

Certified Kubernetes Administrator
Issued by: Cloud Native Computing Foundation
Date: January 2022

LANGUAGES
English (Native)
Spanish (Professional)
Mandarin (Basic)
"""

def test_parser():
    """Test the resume parser with sample resume."""
    parser = ResumeParser()
    
    print("Testing ResumeParser with sample resume...")
    print("=" * 60)
    
    # Parse the resume
    resume = parser.parse_text(test_resume)
    
    # Print results
    print("\n1. CONTACT INFORMATION")
    print("-" * 30)
    print(f"Name: {resume.contact_info.name}")
    print(f"Email: {resume.contact_info.email}")
    print(f"Phone: {resume.contact_info.phone}")
    print(f"Location: {resume.contact_info.address}")
    print(f"LinkedIn: {resume.contact_info.linkedin}")
    print(f"GitHub: {resume.contact_info.github}")
    print(f"Confidence: {resume.confidence_scores.get('contact_info', 0):.2f}")
    
    print("\n2. SUMMARY")
    print("-" * 30)
    if resume.summary:
        print(resume.summary[:100] + "..." if len(resume.summary) > 100 else resume.summary)
    print(f"Confidence: {resume.confidence_scores.get('summary', 0):.2f}")
    
    print("\n3. EXPERIENCE")
    print("-" * 30)
    for i, exp in enumerate(resume.experience):
        print(f"\nExperience {i+1}:")
        print(f"  Title: {exp.title}")
        print(f"  Company: {exp.company}")
        print(f"  Location: {exp.location}")
        print(f"  Duration: {exp.start_date} - {exp.end_date or 'Present'}")
        if exp.responsibilities:
            print(f"  Responsibilities: {len(exp.responsibilities)} items")
    print(f"\nTotal experiences: {len(resume.experience)}")
    print(f"Confidence: {resume.confidence_scores.get('experience', 0):.2f}")
    
    print("\n4. EDUCATION")
    print("-" * 30)
    for edu in resume.education:
        print(f"Degree: {edu.degree}")
        print(f"Institution: {edu.institution}")
        print(f"Graduation: {edu.graduation_date}")
        print(f"GPA: {edu.gpa}")
        print(f"Location: {edu.location}")
    print(f"Confidence: {resume.confidence_scores.get('education', 0):.2f}")
    
    print("\n5. SKILLS")
    print("-" * 30)
    skills_by_category = {}
    for skill in resume.skills:
        category = skill.category or 'Other'
        if category not in skills_by_category:
            skills_by_category[category] = []
        skills_by_category[category].append(skill.name)
    
    for category, skills in skills_by_category.items():
        print(f"{category}: {', '.join(skills[:5])}{'...' if len(skills) > 5 else ''}")
    print(f"\nTotal skills: {len(resume.skills)}")
    print(f"Confidence: {resume.confidence_scores.get('skills', 0):.2f}")
    
    print("\n6. PROJECTS")
    print("-" * 30)
    for proj in resume.projects:
        print(f"Project: {proj.name}")
        if proj.technologies:
            print(f"Technologies: {', '.join(proj.technologies)}")
    print(f"Total projects: {len(resume.projects)}")
    
    print("\n7. CERTIFICATIONS")
    print("-" * 30)
    for cert in resume.certifications:
        print(f"Certification: {cert.name}")
        print(f"Issuer: {cert.issuer}")
        print(f"Date: {cert.issue_date}")
    print(f"Total certifications: {len(resume.certifications)}")
    
    print("\n8. LANGUAGES")
    print("-" * 30)
    print(f"Languages: {', '.join(resume.languages)}")
    
    print("\n9. EXTRACTION METADATA")
    print("-" * 30)
    print(json.dumps(resume.extraction_metadata, indent=2))
    
    print("\n10. OVERALL CONFIDENCE SCORES")
    print("-" * 30)
    for section, score in resume.confidence_scores.items():
        print(f"{section}: {score:.2f}")

if __name__ == "__main__":
    test_parser()