"""
Quality Control - Check generated content for quality issues
"""
import re

def check_quality(content: str, section_title: str) -> dict:
    """
    Check content quality and return issues found.
    
    Returns:
        dict with 'passed', 'warnings', and 'errors'
    """
    warnings = []
    errors = []
    
    # Check 1: Bullet points
    bullet_patterns = [
        r'^\s*[-*•]\s+',  # - or * or • at start of line
        r'^\s*\d+\.\s+',  # Numbered lists
    ]
    
    lines = content.split('\n')
    bullet_count = 0
    for i, line in enumerate(lines, 1):
        for pattern in bullet_patterns:
            if re.match(pattern, line):
                bullet_count += 1
                if bullet_count <= 3:  # Only report first 3
                    warnings.append(f"Line {i}: Bullet point detected: {line[:50]}...")
    
    if bullet_count > 0:
        errors.append(f"Found {bullet_count} bullet points (should be prose only)")
    
    # Check 2: Figures
    figure_count = len(re.findall(r'Figure \d+\.\d+:', content, re.IGNORECASE))
    if figure_count == 0:
        warnings.append("No figures found (should have 2-3 per subsection)")
    elif figure_count < 2:
        warnings.append(f"Only {figure_count} figure(s) found (should have 2-3)")
    
    # Check 3: Tables
    table_count = len(re.findall(r'Table \d+\.\d+:', content, re.IGNORECASE))
    if table_count == 0:
        warnings.append("No tables found (should have 1-2 per subsection)")
    
    # Check 4: ASCII diagrams
    ascii_patterns = [
        r'[┌┐└┘├┤┬┴┼]',  # Box drawing
        r'[→←↑↓⇒⇐⇔]',   # Arrows
    ]
    has_ascii = any(re.search(pattern, content) for pattern in ascii_patterns)
    if not has_ascii:
        warnings.append("No ASCII diagrams found")
    
    # Check 5: Word count
    word_count = len(content.split())
    if word_count < 800:
        errors.append(f"Too short: {word_count} words (target: 1000+)")
    elif word_count < 900:
        warnings.append(f"Slightly short: {word_count} words (target: 1000+)")
    
    # Check 6: Figure explanations
    figure_explanations = re.findall(r'Figure \d+\.\d+:.*?(?=Figure \d+\.\d+:|Table \d+\.\d+:|$)', content, re.DOTALL | re.IGNORECASE)
    for i, expl in enumerate(figure_explanations, 1):
        expl_words = len(expl.split())
        if expl_words < 150:
            warnings.append(f"Figure {i} explanation too short ({expl_words} words, need 150+)")
    
    # Check 7: Table explanations
    table_explanations = re.findall(r'Table \d+\.\d+:.*?(?=Figure \d+\.\d+:|Table \d+\.\d+:|$)', content, re.DOTALL | re.IGNORECASE)
    for i, expl in enumerate(table_explanations, 1):
        expl_words = len(expl.split())
        if expl_words < 150:
            warnings.append(f"Table {i} explanation too short ({expl_words} words, need 150+)")
    
    passed = len(errors) == 0
    
    return {
        'passed': passed,
        'warnings': warnings,
        'errors': errors,
        'stats': {
            'word_count': word_count,
            'figure_count': figure_count,
            'table_count': table_count,
            'has_ascii': has_ascii,
            'bullet_count': bullet_count
        }
    }

def print_quality_report(report: dict, subsection_title: str):
    """Print quality report to console."""
    stats = report['stats']
    
    print(f"\n      📊 Quality Check: {subsection_title}")
    print(f"         Words: {stats['word_count']} | Figures: {stats['figure_count']} | Tables: {stats['table_count']}")
    
    if report['errors']:
        print(f"         ❌ ERRORS:")
        for error in report['errors']:
            print(f"            - {error}")
    
    if report['warnings']:
        print(f"         ⚠️  WARNINGS:")
        for warning in report['warnings'][:3]:  # Show first 3
            print(f"            - {warning}")
        if len(report['warnings']) > 3:
            print(f"            ... and {len(report['warnings']) - 3} more")
    
    if report['passed'] and not report['warnings']:
        print(f"         ✅ All checks passed!")
