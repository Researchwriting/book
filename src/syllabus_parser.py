"""
Syllabus Parser - Reads the input syllabus and extracts sections
"""
from typing import List, Dict
import re

def parse_syllabus(filepath: str) -> List[Dict[str, str]]:
    """
    Parse syllabus.md and extract chapter and section information.
    
    Supports two formats:
    1. Markdown: # Chapter\n## 1. Section
    2. Plain text: Chapter Title\n    1. Section
    
    Returns:
        List of dicts with 'chapter', 'section_number', 'section_title'
    """
    sections = []
    current_chapter = ""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            original_line = line
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Format 1: Markdown headers
            if line.startswith('# '):
                current_chapter = line[2:].strip()
            elif line.startswith('## '):
                section_text = line[3:].strip()
                parts = section_text.split('.', 1)
                if len(parts) == 2:
                    section_number = parts[0].strip()
                    section_title = parts[1].strip()
                    sections.append({
                        'chapter': current_chapter,
                        'section_number': section_number,
                        'section_title': section_title
                    })
            
            # Format 2: Plain text (indented or numbered)
            elif not line.startswith('#'):
                # Check if it's a chapter (no leading spaces/numbers)
                if not original_line.startswith(' ') and not original_line.startswith('\t'):
                    # Remove "Chapter X:" prefix if present
                    if line.lower().startswith('chapter'):
                        current_chapter = re.sub(r'^chapter\s+\d+:\s*', '', line, flags=re.IGNORECASE)
                    else:
                        current_chapter = line
                
                # Check if it's a section (starts with number or indented)
                elif re.match(r'^\s*(\d+)\.\s+(.+)', line):
                    match = re.match(r'^\s*(\d+)\.\s+(.+)', line)
                    if match:
                        section_number = match.group(1)
                        section_title = match.group(2).strip()
                        # Remove trailing notes in parentheses if they're just comments
                        section_title = re.sub(r'\s*\([^)]*we should.*\)\.?$', '', section_title, flags=re.IGNORECASE)
                        sections.append({
                            'chapter': current_chapter,
                            'section_number': section_number,
                            'section_title': section_title
                        })
    
    return sections

