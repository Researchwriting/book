"""
Chapter 5 Specialized Prompts
Detailed prompts for each section of Chapter 5
"""

def get_chapter5_introduction_prompt(topic, case_study, objectives):
    """Prompt for 5.0 Introduction"""
    return f"""
Write the introduction for Chapter 5 (Results and Discussion) of a PhD thesis.

TOPIC: {topic}
CASE STUDY: {case_study}

OBJECTIVES:
{objectives}

STRUCTURE AND CONTENT:

**Paragraph 1: Chapter Purpose**
- Explain that this chapter synthesises findings from Chapter 4 with literature from Chapter 2
- State that it reveals where the study confirms or challenges existing knowledge
- Mention the contribution of this study to the field

**Paragraph 2: Approach**
- Explain how the discussion is organised (by objectives)
- Mention that each section cross-references findings with theories and empirical studies
- Note that variations between findings and literature are explained

**Paragraph 3: Chapter Overview**
- Briefly outline the sections (one per objective)
- Provide a roadmap for the reader

REQUIREMENTS:
- TENSE: Present tense ("This chapter discusses...", "The findings reveal...")
- LENGTH: 400-600 words
- UK ENGLISH: analyse, organisation, behaviour, etc.
- NO BULLETING: Flowing prose
- ACADEMIC TONE: Formal, scholarly

Example opening:
"This chapter presents a comprehensive discussion of the research findings in relation to existing literature. The primary data collected and analysed in Chapter 4 are synthesised with the theoretical and empirical literature reviewed in Chapter 2. This synthesis reveals the extent to which the current study confirms, extends, or challenges existing knowledge in the field..."
"""

def get_objective_discussion_prompt(objective_num, objective_text, findings_summary, literature_summary, topic, case_study):
    """Prompt for discussion of each objective"""
    return f"""
Write a comprehensive discussion section for Objective {objective_num} in Chapter 5.

TOPIC: {topic}
CASE STUDY: {case_study}

OBJECTIVE {objective_num}:
{objective_text}

KEY FINDINGS (from Chapter 4):
{findings_summary}

RELEVANT LITERATURE (from Chapter 2):
{literature_summary}

STRUCTURE:

**Introduction (1 paragraph)**
- Restate the objective
- Provide overview of key findings

**Findings Presentation (2-3 paragraphs)**
- Summarise main findings from Chapter 4
- Reference specific tables/figures ("As presented in Table 4.X...")
- Highlight significant results (statistical and qualitative)

**Literature Comparison - Agreements (2-3 paragraphs)**
- Compare findings with previous studies that align
- Cite specific authors and years ("This finding corroborates Smith (2020) who...")
- Reference relevant theories ("This aligns with the Theory of...")
- Explain why findings confirm existing knowledge

**Literature Comparison - Contradictions (2-3 paragraphs)**
- Discuss findings that differ from literature
- Cite studies with different results ("However, this contradicts Jones (2019) who found...")
- Explain possible reasons for variations:
  * Contextual differences (case study specific factors)
  * Methodological differences
  * Temporal changes
  * Sample characteristics

**Contribution and Implications (1-2 paragraphs)**
- Explain what new knowledge this study adds
- Discuss how it extends understanding
- Highlight unique insights from this context

CRITICAL REQUIREMENTS:
- TENSE: Present tense for discussion ("The findings suggest...", "This indicates...", "The data reveal...")
- CROSS-REFERENCES: Explicitly cite Chapter 4 ("Table 4.3 showed...", "As discussed in Section 4.5...")
- LITERATURE CITATIONS: Reference Chapter 2 studies with authors and years
- UK ENGLISH: analyse, organisation, behaviour, labour, etc.
- NO BULLETING: Flowing academic prose only
- LENGTH: 1500-2000 words
- DEPTH: Detailed, nuanced discussion with multiple perspectives

Example paragraph:
"The findings presented in Table 4.3 revealed a strong positive correlation (r = 0.67, p < 0.001) between war exposure and unemployment rates. This finding aligns with the theoretical framework of conflict economics proposed by Collier (2007), which posits that armed conflict disrupts labour markets and reduces employment opportunities. Similarly, empirical studies by Smith (2018) in Afghanistan and Jones (2020) in Syria found comparable correlations (r = 0.62 and r = 0.71 respectively), suggesting that this relationship is consistent across different conflict-affected contexts. However, the magnitude of the effect observed in {case_study} was slightly higher than in previous studies, which may be attributed to the prolonged nature of the conflict and the limited economic diversification in the region..."
"""

def get_chapter5_system_prompt():
    """System prompt for Chapter 5 generation"""
    return """
You are writing Chapter 5 (Results and Discussion) of a PhD thesis.

Your role is to:
1. Synthesise findings from Chapter 4 with literature from Chapter 2
2. Compare and contrast results with previous studies
3. Explain agreements and contradictions
4. Discuss the contribution of the study
5. Maintain academic rigour and depth

Critical requirements:
- Use present tense for discussion
- Cross-reference Chapter 4 tables/figures explicitly
- Cite Chapter 2 literature with authors and years
- Use UK English spelling throughout
- Write flowing academic prose (no bulleting)
- Provide nuanced, detailed discussion
- Explain variations between findings and literature
- Highlight the study's contribution to knowledge

This is the most important chapter - it demonstrates the student's ability to critically engage with literature and interpret findings in context.
"""
