"""
Special prompts for Chapter 2 Literature Review
Handles the rigorous synthesis requirements for academic literature.
"""

def get_chapter2_theory_prompt(section_title, topic, case_study, citation_guide):
    """Prompt for 2.2 Theoretical Framework sections"""
    return f"""
You are writing the Theoretical Framework section of a PhD thesis.

TOPIC: {topic}
CASE STUDY: {case_study}
SECTION: {section_title}

CITATION GUIDE (Use ONLY these sources):
{citation_guide}

REQUIREMENTS FOR EACH THEORY:
1. **Historical Background**: Origins and development of the theory
2. **Supporting Studies**: Studies that used and validated this theory (with methodology and findings)
3. **Criticisms**: Scholars who critique the theory and their arguments
4. **Relevance**: How this theory relates to your study objectives
5. **Gaps**: What the theory doesn't explain in your context
6. **Visual Representation**: Create an ASCII diagram showing the theory in context
7. **Caption and Source**: Provide figure caption and source
8. **Interpretation**: Detailed explanation of the visual (3-4 paragraphs)

FORMAT:
Use subsections (2.2.1, 2.2.2, etc.) for each theory.

CITATIONS: Use (Author, Year) format only. Group citations at end of paragraphs.
**STRICT PROHIBITION**: DO NOT INVENT OR HALLUCINATE CITATIONS. If a source is not in the CITATION GUIDE, DO NOT CITE IT.
**CRITICAL**: DO NOT add a "References" or "Bibliography" section at the end. Only use in-text citations.

CRITICAL: DO NOT include the section heading/title in your response - it will be added automatically.
Start directly with the first paragraph of content.

Write approximately 2000-2500 words for this section.
"""

def get_chapter2_theme_prompt(section_title, topic, case_study, citation_guide):
    """Prompt for 2.3-2.6 Theme sections with rigorous synthesis"""
    return f"""
You are writing a Literature Review theme section for a PhD thesis.

TOPIC: {topic}
CASE STUDY: {case_study}
SECTION: {section_title}

CITATION GUIDE (Use ONLY these sources):
{citation_guide}

CRITICAL REQUIREMENT - 5-STEP PARAGRAPH PROCESS:
Every paragraph MUST follow this exact structure:

**Step 1: Thematic Sentence**
Start with a clear topic sentence stating the specific finding or debate.

**Step 2: Detail the Anchor Study**
- Introduce: "A seminal study by Author A (Year) investigated..."
- Methodology: "Employing a quantitative approach with N=[sample size], the study used [specific method, e.g., OLS regression]..."
- Detailed Findings: "The descriptive statistics revealed [specific percentages/numbers]. The regression analysis showed [β values, p-values, R²]. For example, β = 0.34, p < 0.05..."
  OR for qualitative: "Through in-depth interviews with N=[number], the study identified [specific themes/patterns]..."

**Step 3: Critical Analysis**
- State implication: "The findings from Author A (Year) provide strong empirical evidence for..."
- Identify gap IN YOUR OWN WORDS: "However, the study's quantitative nature fails to explain WHY... Furthermore, its focus on [context] means findings may not transfer to {case_study}. This highlights a gap for..."

**Step 4: Synthesize Supporting/Contrasting Studies**
- "This finding is supported by Author B (Year), who using [method] in [context], found that [specific results]..."
- "In contrast, Author C (Year) in [context] suggested that [different finding]..."

**Step 5: Grouped Citation**
End paragraph: (Author A, Year; Author B, Year; Author C, Year)

STRUCTURE:
- Brief introduction (1 paragraph)
- 3 subsections (2.X.1, 2.X.2, 2.X.3)
- Each subsection: 7-12 detailed paragraphs following the 5-step process
- Each paragraph: 200-300 words

TOTAL LENGTH: 4000-5000 words for this section.

CITATIONS: Use (Author, Year) format. Always group at end of paragraphs.
**STRICT PROHIBITION**: DO NOT INVENT OR HALLUCINATE CITATIONS. If a source is not in the CITATION GUIDE, DO NOT CITE IT.
**CRITICAL**: DO NOT add a "References" or "Bibliography" section at the end. Only use in-text citations.

CRITICAL: DO NOT include the section heading/title in your response - it will be added automatically.
Start directly with the first paragraph of content.
"""

def get_chapter2_gap_prompt(section_title, topic, case_study, citation_guide):
    """Prompt for 2.7 Literature Gap section"""
    return f"""
You are writing the Literature Gap section of a PhD thesis.

TOPIC: {topic}
CASE STUDY: {case_study}
SECTION: {section_title}

CITATION GUIDE (Use ONLY these sources):
{citation_guide}

REQUIREMENTS:
1. **Strong Gap Identification**: Clearly articulate what is missing in the literature
2. **Literature Matrix Table**: Create a comprehensive table with columns:
   - Author(s) & Year
   - Study Focus
   - Methodology
   - Key Findings
   - Limitations/Gaps
   - Relevance to Current Study

FORMAT THE TABLE IN MARKDOWN:
| Author(s) & Year | Study Focus | Methodology | Key Findings | Limitations/Gaps | Relevance |
|-----------------|-------------|-------------|--------------|------------------|-----------|
| Smith (2023) | ... | Quantitative, N=500 | β=0.45, p<0.01 | Limited to urban areas | ... |

3. **Synthesis**: After the table, write 3-4 paragraphs synthesizing the gaps
4. **Justification**: Explain how your study addresses these gaps
5. **STRICT PROHIBITION**: DO NOT INVENT OR HALLUCINATE CITATIONS. If a source is not in the CITATION GUIDE, DO NOT CITE IT.
6. **CRITICAL**: DO NOT add a "References" or "Bibliography" section at the end. Only use in-text citations.

LENGTH: 1500-2000 words

CITATIONS: Use (Author, Year) format.

CRITICAL: DO NOT include the section heading/title in your response - it will be added automatically.
Start directly with the first paragraph of content.
"""
