"""
Master Command Generator - Creates detailed prompts for each section
"""
from typing import Dict

def generate_master_command(section_info: Dict[str, str]) -> str:
    """
    Generate a Master Command prompt for a specific section.
    
    Args:
        section_info: Dict with 'chapter', 'section_number', 'section_title'
    
    Returns:
        Complete Master Command prompt
    """
    chapter = section_info['chapter']
    section_num = section_info['section_number']
    section_title = section_info['section_title']
    
    master_command = f"""# MASTER COMMAND FOR SECTION {section_num}

## {section_title}

> **PROMPT (COPY–PASTE EXACTLY):**
>
> Write a **complete, 40,000–50,000-word** university-level textbook chapter section for:
>
> **{chapter}**
> **Section {section_num}: {section_title}**
>
> ### 🔒 ABSOLUTE LANGUAGE RULE
>
> * **Use English ONLY.**
> * **Do NOT use Chinese characters, Japanese, Korean, Arabic, or any non-English scripts.**
> * All writing, headings, labels, figure placeholders, and examples must be in **English only**.
>
> ### 🎯 GENERAL REQUIREMENTS
>
> * Audience: **Postgraduate social science students**, especially in **African and South Sudan contexts**.
> * Tone: **Teaching-focused, clear, practical, step-by-step**.
> * Purpose: Teach students **how to understand and apply {section_title}**, not just define concepts.
> * Include **figures**, **tables**, **toolkits**, **examples**, **checklists**, and **practical exercises**.
> * Use **APA 7th Edition** for any citations.
> * Include **25+ references (2019–2025)** if needed.
>
> ### 📘 CONTENT OUTLINE
>
> Expand the following structure thoroughly (each subsection should be 2,000-4,000 words):
>
> #### {section_num}.1 Introduction to {section_title}
>
> * Define key concepts and terminology
> * Explain the importance and relevance
> * Provide context for African/South Sudan research
> * Preview what will be covered
> * Insert: Figure {section_num}.1: Overview of {section_title}
>
> ---
>
> #### {section_num}.2 Theoretical and Conceptual Foundations
>
> * Explain underlying theories and frameworks
> * Discuss philosophical assumptions
> * Connect to broader research methodology
> * Insert: Figure {section_num}.2: Theoretical Framework
>
> ---
>
> #### {section_num}.3 [Core Concept 1 of {section_title}]
>
> * Explain this core component in detail
> * Provide examples and applications
> * Insert: Table {section_num}.1: Key Concepts Comparison
>
> ---
>
> #### {section_num}.4 [Core Concept 2 of {section_title}]
>
> * Deep dive into this specific aspect
> * Practical relevance
> * Insert: Figure {section_num}.3: Process Flow
>
> ---
>
> #### {section_num}.5 [Core Concept 3 of {section_title}]
>
> * Detailed explanation and analysis
> * Insert: Figure {section_num}.4: Detailed Diagram
>
> ---
>
> #### {section_num}.6 Practical Application and Implementation
>
> * Step-by-step guide to applying {section_title}
> * Real-world examples from African contexts
> * Common challenges and solutions
> * Insert: Figure {section_num}.5: Implementation Workflow
>
> ---
>
> #### {section_num}.7 Tools, Techniques, and Best Practices
>
> * Specific tools and resources
> * Techniques for effective implementation
> * Best practices and quality standards
> * Insert: Table {section_num}.2: Tools and Techniques
>
> ---
>
> #### {section_num}.8 Ethical Considerations and Challenges
>
> * Ethical issues specific to {section_title}
> * Cultural sensitivity in African contexts
> * Addressing common challenges
> * Insert: Figure {section_num}.6: Ethical Decision-Making Framework
>
> ---
>
> #### {section_num}.9 Case Studies and Examples
>
> * Detailed case studies from African/South Sudan research
> * Analysis of successful applications
> * Lessons learned
> * Insert: Table {section_num}.3: Case Study Analysis
>
> ---
>
> #### {section_num}.10 Integration with Other Methods
>
> * How {section_title} relates to other approaches
> * Combining with other methods
> * Complementary techniques
>
> ---
>
> #### {section_num}.11 Digital Tools and Technology
>
> * Relevant software and digital tools
> * Technology in African contexts
> * Insert: Figure {section_num}.7: Digital Architecture
>
> ---
>
> #### {section_num}.12 Integrating AI Tools
>
> * How AI can assist with {section_title}
> * Specific prompts and use cases
> * Limitations and ethical warnings
> * Insert: Figure {section_num}.8: AI-Assisted Workflow
>
> ---
>
> #### {section_num}.13 Quality Assurance and Reliability
>
> * Ensuring quality and validity
> * Checking for errors
> * Insert: Figure {section_num}.9: QA Process
>
> ---
>
> #### {section_num}.14 Common Mistakes and How to Avoid Them
>
> * Typical errors students make
> * Misconceptions and pitfalls
> * Corrective strategies
> * Insert: Figure {section_num}.10: Common Errors and Solutions
>
> ---
>
> #### {section_num}.15 Practical Exercises and Skill Building
>
> * Include several hands-on tasks:
> * Exercise 1: [Specific task related to {section_title}]
> * Exercise 2: [Analysis or evaluation task]
> * Exercise 3: [Design or planning task]
> * Exercise 4: [Critical thinking task]
> * Exercise 5: [Application task]
> * Insert: Figure {section_num}.11: Practice Workflow
>
> ---
>
> #### {section_num}.16 Summary, Learning Outcomes, and Reflection
>
> * Clear summary of key concepts
> * List 7-10 learning outcomes
> * Include 15+ reflection questions
> * Suggest further reading
>
> ---
>
> ### 📊 VISUALS
>
Include **10–12 figures** and **3–5 tables**, described textually (no Chinese symbols).
>
> ### 🧭 STYLE
>
> * CLEAR, practical, step-by-step
> * Lots of examples, especially from African/South Sudan research contexts
> * No bullet points in main text - use full paragraphs and flowing prose
> * No non-English characters anywhere
> * Teaching tone throughout
>
> Now generate the full, coherent, publication-ready 40,000–50,000-word section.
"""
    
    return master_command
