"""
Resume parsing: extract raw text from PDF/DOCX/TXT, then pull out
skills, contact info, resume sections, and structural signals
(bullet points, action verbs, word count) used by the ATS scorer.
"""
import re
import io
from pypdf import PdfReader
import docx

from .skill_data import ALIAS_LOOKUP, ALL_TERMS, normalize

SECTION_PATTERNS = {
    'Contact Info': re.compile(r'email|phone|contact', re.I),
    'Education': re.compile(r'education|academic|b\.?tech|b\.?e\.?|degree|university|college', re.I),
    'Skills': re.compile(r'skills|technical skills|competenc', re.I),
    'Experience / Projects': re.compile(r'experience|projects|internship|work history', re.I),
    'Certifications': re.compile(r'certification|certificate|course completed', re.I),
}

ACTION_VERBS = [
    'developed', 'built', 'designed', 'implemented', 'created', 'led', 'managed',
    'analyzed', 'optimized', 'automated', 'deployed', 'collaborated', 'improved',
    'launched', 'achieved', 'reduced', 'increased', 'tested', 'integrated', 'maintained'
]

BULLET_LINE_RE = re.compile(r'^[ \t]*[•\-\*▪●][ \t]', re.M)
EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
PHONE_RE = re.compile(r'(?:\+?\d{1,3}[-.\s]?)?\d{10}')
LINKEDIN_RE = re.compile(r'linkedin\.com/[a-zA-Z0-9\-/_]+', re.I)
GITHUB_RE = re.compile(r'github\.com/[a-zA-Z0-9\-/_]+', re.I)


def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    return '\n'.join((page.extract_text() or '') for page in reader.pages)


def extract_text_from_docx(file_bytes: bytes) -> str:
    document = docx.Document(io.BytesIO(file_bytes))
    return '\n'.join(p.text for p in document.paragraphs)


def extract_text(filename: str, file_bytes: bytes) -> str:
    name = filename.lower()
    if name.endswith('.pdf'):
        return extract_text_from_pdf(file_bytes)
    if name.endswith('.docx'):
        return extract_text_from_docx(file_bytes)
    if name.endswith('.txt'):
        return file_bytes.decode('utf-8', errors='ignore')
    raise ValueError('Unsupported file type. Please upload a PDF, DOCX, or TXT file.')


def extract_skills(text: str):
    cleaned = ' ' + normalize(text) + ' '
    found = set()
    for term in ALL_TERMS:
        if len(term) > 1 and f' {term} ' in cleaned:
            found.add(ALIAS_LOOKUP[term])
    return sorted(found)


def extract_contact(text: str):
    email = EMAIL_RE.search(text)
    phone = PHONE_RE.search(text)
    linkedin = LINKEDIN_RE.search(text)
    github = GITHUB_RE.search(text)
    return {
        'email': email.group(0) if email else None,
        'phone': phone.group(0) if phone else None,
        'linkedin': linkedin.group(0) if linkedin else None,
        'github': github.group(0) if github else None,
    }


def extract_sections(text: str):
    return {label: bool(pattern.search(text)) for label, pattern in SECTION_PATTERNS.items()}


def count_structure_signals(text: str):
    bullet_lines = len(BULLET_LINE_RE.findall(text))
    lower = text.lower()
    verb_hits = sum(1 for v in ACTION_VERBS if v in lower)
    return {'bulletLines': bullet_lines, 'verbHits': verb_hits}


def word_count(text: str) -> int:
    return len(re.findall(r'\S+', text.strip()))


def analyze_resume_text(text: str) -> dict:
    return {
        'rawText': text,
        'skills': extract_skills(text),
        'contact': extract_contact(text),
        'sections': extract_sections(text),
        'structure': count_structure_signals(text),
        'words': word_count(text),
    }
