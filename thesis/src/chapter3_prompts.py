"""
Special prompts for Chapter 3 Research Methodology
Handles detailed methodology requirements with tables, formulas, and calculations.
"""

def get_chapter3_introduction_prompt(section_title, topic, case_study, citation_guide, objectives):
    """Prompt for 3.1 Introduction"""
    return f"""
You are writing the Introduction section of the Research Methodology chapter.

TOPIC: {topic}
CASE STUDY: {case_study}
SECTION: {section_title}

RESEARCH OBJECTIVES:
{objectives}

CITATION GUIDE (Use ONLY these sources):
{citation_guide}

REQUIREMENTS:
1. **Remind the Reader**: Briefly restate the research problem from Chapter 1
2. **Chapter Overview**: Explain what this chapter covers (research philosophy, design, population, sampling, data collection, analysis, ethics)
3. **Justification**: Why this methodology is appropriate for addressing the objectives
4. **Structure**: Outline the sections in this chapter
5. **STRICT PROHIBITION**: DO NOT INVENT OR HALLUCINATE CITATIONS. If a source is not in the CITATION GUIDE, DO NOT CITE IT.
6. **CRITICAL**: DO NOT add a "References" or "Bibliography" section at the end. Only use in-text citations.

LENGTH: 800-1000 words

CITATIONS: Use (Author, Year) format.

CRITICAL: DO NOT include the section heading/title in your response - it will be added automatically.
Start directly with the first paragraph of content.
"""

def get_chapter3_population_prompt(section_title, topic, case_study, citation_guide, objectives):
    """Prompt for 3.4 Target Population with table"""
    return f"""
You are writing the Target Population section of the Research Methodology chapter.

TOPIC: {topic}
CASE STUDY: {case_study}
SECTION: {section_title}

RESEARCH OBJECTIVES:
{objectives}

CITATION GUIDE (Use ONLY these sources):
{citation_guide}

REQUIREMENTS:
1. **Define Target Population**: Who/what constitutes your population
2. **Justify Selection**: Why this population is relevant to your objectives
3. **Population Characteristics**: Demographics, size, location
4. **Accessibility**: How you can access this population

5. **MANDATORY TABLE 3.1: Study Population Distribution**
Create a markdown table with the following structure:

| Category | Sub-category | Population Size | Percentage (%) |
|----------|--------------|-----------------|----------------|
| [Category 1] | [Sub 1] | [Number] | [%] |
| [Category 1] | [Sub 2] | [Number] | [%] |
| [Category 2] | [Sub 1] | [Number] | [%] |
| **Total** | | [Total Number] | **100%** |

**Table 3.1:** Study Population Distribution
*Source: [Specify source, e.g., Ministry of X, 2023; Field Survey, 2024]*

6. **Interpretation**: After the table, provide 2-3 paragraphs interpreting the distribution
7. **STRICT PROHIBITION**: DO NOT INVENT OR HALLUCINATE CITATIONS. If a source is not in the CITATION GUIDE, DO NOT CITE IT.
8. **CRITICAL**: DO NOT add a "References" or "Bibliography" section at the end. Only use in-text citations.

LENGTH: 1500-2000 words (including table)

CITATIONS: Use (Author, Year) format.

CRITICAL: DO NOT include the section heading/title in your response - it will be added automatically.
Start directly with the first paragraph of content.
"""

def get_chapter3_sample_size_prompt(section_title, topic, case_study, citation_guide, objectives):
    """Prompt for 3.6 Sample Size with formulas and calculations"""
    return f"""
You are writing the Sample Size section of the Research Methodology chapter.

TOPIC: {topic}
CASE STUDY: {case_study}
SECTION: {section_title}

RESEARCH OBJECTIVES:
{objectives}

CITATION GUIDE (Use ONLY these sources):
{citation_guide}

REQUIREMENTS:
1. **Sample Size Determination**: Explain the approach used
2. **Formula**: Present the sample size formula used. For example:

For finite population:
```
n = (Z² × p × q × N) / (e² × (N-1) + Z² × p × q)

Where:
- n = sample size
- Z = Z-score (1.96 for 95% confidence level)
- p = estimated proportion (0.5 for maximum variability)
- q = 1 - p
- N = population size
- e = margin of error (0.05 for 5%)
```

3. **Calculations**: Show step-by-step calculations with actual numbers
Example:
```
Given:
- N = 5,000 (total population)
- Z = 1.96 (95% confidence)
- p = 0.5
- q = 0.5
- e = 0.05

Calculation:
n = (1.96² × 0.5 × 0.5 × 5000) / (0.05² × (5000-1) + 1.96² × 0.5 × 0.5)
n = (3.8416 × 0.25 × 5000) / (0.0025 × 4999 + 0.9604)
n = 4801 / 13.4579
n ≈ 357
```

4. **MANDATORY TABLE 3.2: Sample Size Distribution and Sampling Methods**
Create a markdown table:

| Stratum/Category | Population (N) | Sample Size (n) | Sampling Method | Justification |
|------------------|----------------|-----------------|-----------------|---------------|
| [Category 1] | [Number] | [Number] | [Method] | [Why this method] |
| [Category 2] | [Number] | [Number] | [Method] | [Why this method] |
| **Total** | **[Total N]** | **[Total n]** | | |

**Table 3.2:** Sample Size Distribution and Sampling Methods
*Source: Researcher's Computation, 2024*

5. **Interpretation**: Explain the distribution and justify the methods
6. **STRICT PROHIBITION**: DO NOT INVENT OR HALLUCINATE CITATIONS. If a source is not in the CITATION GUIDE, DO NOT CITE IT.
7. **CRITICAL**: DO NOT add a "References" or "Bibliography" section at the end. Only use in-text citations.

LENGTH: 2000-2500 words (including formulas, calculations, and table)

CITATIONS: Use (Author, Year) format for sampling formulas (e.g., Yamane, 1967; Cochran, 1977).

CRITICAL: DO NOT include the section heading/title in your response - it will be added automatically.
Start directly with the first paragraph of content.
"""

def get_chapter3_detailed_prompt(section_title, topic, case_study, citation_guide, objectives):
    """Prompt for other detailed Chapter 3 sections"""
    return f"""
You are writing a detailed Research Methodology section.

TOPIC: {topic}
CASE STUDY: {case_study}
SECTION: {section_title}

RESEARCH OBJECTIVES:
{objectives}

CITATION GUIDE (Use ONLY these sources):
{citation_guide}

REQUIREMENTS:
1. **Be Detailed**: Provide comprehensive explanation
2. **Justify Choices**: Explain why this approach/method is appropriate for your study
3. **Link to Objectives**: Show how this section supports achieving the research objectives
4. **Academic Rigor**: Use proper academic language and cite relevant methodological literature
5. **Practical Details**: Include specific details about implementation
6. **STRICT PROHIBITION**: DO NOT INVENT OR HALLUCINATE CITATIONS. If a source is not in the CITATION GUIDE, DO NOT CITE IT.
7. **CRITICAL**: DO NOT add a "References" or "Bibliography" section at the end. Only use in-text citations.

SPECIFIC GUIDANCE BY SECTION:
- **3.2 Research Philosophy**: Discuss positivism/interpretivism/pragmatism, justify your choice
- **3.3 Research Design**: Descriptive/exploratory/explanatory/causal, quantitative/qualitative/mixed
- **3.5 Sampling Design**: Probability/non-probability, specific techniques, justification
- **3.7 Data Collection Instruments**: Questionnaires/interviews/observations, design, pilot testing
- **3.8 Validity and Reliability**: Cronbach's alpha, content validity, construct validity, test-retest
- **3.9 Data Collection Procedures**: Step-by-step process, primary vs secondary data sources
- **3.10 Data Analysis Procedures**: Statistical tests, software (SPSS/R/Stata), thematic analysis
- **3.11 Ethical Considerations**: Informed consent, confidentiality, anonymity, ethical approval

LENGTH: 1500-2000 words

CITATIONS: Use (Author, Year) format. Cite methodological authorities.

CRITICAL: DO NOT include the section heading/title in your response - it will be added automatically.
Start directly with the first paragraph of content.
"""
