"""
Textbook Writer - Generates academic content following Master Command style
"""
from src.generator import LLMGenerator

def write_subsection(
    generator: LLMGenerator,
    section_title: str,
    topic_title: str,
    subsection_title: str,
    target_words: int = 1000
) -> str:
    """
    Write a subsection of the textbook.
    
    Args:
        generator: LLM generator
        section_title: Parent section
        topic_title: Parent topic
        subsection_title: Current subsection
        target_words: Target word count
    
    Returns:
        Generated content
    """
    prompt = f"""You are writing a university-level textbook for postgraduate social science students, with a focus on African and South Sudan contexts.

SECTION: {section_title}
TOPIC: {topic_title}
SUBSECTION: {subsection_title}

CRITICAL WRITING RULES (FOLLOW EXACTLY):

1. **NO BULLET POINTS OR LISTS** - Write in flowing paragraphs only. Every idea must be expressed in complete sentences within paragraphs. Do not use bullets, numbered lists, or any list formatting in the main text.

2. **PROSE STYLE** - Write like a textbook, not like lecture notes. Each paragraph should flow naturally into the next. Use transition words and phrases to connect ideas.

3. **FIGURES AND TABLES - MANDATORY REQUIREMENTS**:
   
   A. **ASCII ART DIAGRAMS** - Create actual visual diagrams using ASCII characters:
      - Use box-drawing: ┌─┐ │ └─┘ ├ ┤ ┬ ┴ ┼
      - Use arrows: → ← ↑ ↓ ⇒ ⇐ ⇔
      - Use lines: ─ │ ═ ║
   
   B. **FIGURE FORMAT** (Include 2-3 figures per subsection):
      ```
      Figure X.Y: [Descriptive Title]
      
      [ASCII diagram here]
      ┌─────────────────┐
      │   Component A   │
      └────────┬────────┘
               │
               ↓
      ┌─────────────────┐
      │   Component B   │
      └─────────────────┘
      
      Explanation: [2-3 paragraphs explaining what the figure shows, why it matters, 
      how to interpret it, and how it relates to the concepts being taught. This is 
      TEACHING, so explain every element of the figure in detail.]
      ```
   
   C. **TABLE FORMAT** (Include 1-2 tables per subsection):
      ```
      Table X.Y: [Descriptive Title]
      
      ┌──────────────────┬──────────────────┬──────────────────┐
      │ Column Header 1  │ Column Header 2  │ Column Header 3  │
      ├──────────────────┼──────────────────┼──────────────────┤
      │ Data point       │ Data point       │ Data point       │
      │ Data point       │ Data point       │ Data point       │
      └──────────────────┴──────────────────┴──────────────────┘
      
      Explanation: [2-3 paragraphs explaining what the table shows, how to read it,
      what patterns or insights it reveals, and how students should use this 
      information. Explain each column and what the data means.]
      ```
   
   D. **NUMBERING**: Use format "Figure X.Y" or "Table X.Y" where X is section number
   
   E. **EXPLANATIONS**: Every figure and table MUST have a detailed explanation 
      (minimum 150 words) that teaches students how to interpret and use it.

4. **TEACHING TONE** - This is TEACHING, not narration. Explain concepts as if you're 
   helping a student understand, not telling a story. Ask rhetorical questions, 
   anticipate confusion, provide examples.

5. **DEEP EXPLANATIONS** - Don't just define terms. Explain:
   - WHY this concept matters
   - HOW it works in practice
   - WHEN to use it
   - WHAT happens if you don't
   - Real examples from African/South Sudan research

6. **AFRICAN CONTEXT** - Integrate examples from African research, South Sudan contexts, 
   development work, post-conflict settings, and low-resource environments naturally.

7. **LENGTH** - Write approximately {target_words} words. This should be substantial, 
   detailed content with multiple figures and tables.

8. **STRUCTURE** - Use subheadings if needed, but content under each heading must be 
   in paragraph form, never bullets.

EXAMPLE OF GOOD FIGURE EXPLANATION:
"Figure 3.2 illustrates the relationship between research design selection and data 
quality outcomes. The diagram shows how the choice of design (represented in the top 
box) flows through methodological decisions (middle section) to ultimately impact the 
validity and reliability of findings (bottom section). Notice the bidirectional arrows 
between 'Design Choice' and 'Resource Constraints' - this represents the iterative 
nature of design refinement that researchers in low-resource settings often experience. 
When working in South Sudan, for instance, a researcher might initially plan a 
randomized controlled trial but discover that security constraints necessitate a 
quasi-experimental approach instead..."

Now write the complete subsection for "{subsection_title}" following ALL rules above. 
Include at least 2 figures and 1 table with detailed explanations.

Begin writing now:"""

    response = generator.generate(prompt, max_tokens=4000)
    return response

def write_section_introduction(
    generator: LLMGenerator,
    section_title: str,
    topics: list
) -> str:
    """
    Write an introduction for the entire section.
    
    Args:
        generator: LLM generator
        section_title: Section title
        topics: List of Topic objects
    
    Returns:
        Introduction text
    """
    topics_list = ", ".join([t.title for t in topics])
    
    prompt = f"""You are writing a university-level textbook introduction.

SECTION: {section_title}

This section will cover the following topics: {topics_list}

CRITICAL WRITING RULES:
1. **NO BULLET POINTS** - Write in flowing paragraphs only
2. **PROSE STYLE** - Like a textbook, not lecture notes
3. **DEEP CONTEXT** - Explain why this section matters in research methodology
4. **AFRICAN EXAMPLES** - Use examples from African/South Sudan research contexts
5. **LENGTH** - Write 500-800 words

Write a comprehensive introduction that:
- Explains the importance of {section_title} in social science research
- Provides context for why students need to learn this material
- Previews the topics that will be covered (but in prose, not a list)
- Uses African/South Sudan examples where relevant
- Sets an academic, teaching-focused tone

Use English ONLY. No non-English characters.

Write the introduction now in flowing paragraphs:"""

    response = generator.generate(prompt, max_tokens=2000)
    return response

def write_section_summary(
    generator: LLMGenerator,
    section_title: str,
    topics: list
) -> str:
    """
    Write a summary and reflection for the section.
    
    Args:
        generator: LLM generator
        section_title: Section title
        topics: List of Topic objects
    
    Returns:
        Summary text
    """
    topics_list = ", ".join([t.title for t in topics])
    
    prompt = f"""You are writing a university-level textbook section summary.

SECTION: {section_title}

Topics covered: {topics_list}

CRITICAL WRITING RULES:
1. **NO BULLET POINTS** - Write in flowing paragraphs only
2. **PROSE STYLE** - Like a textbook conclusion, not a checklist
3. **SYNTHESIS** - Tie concepts together, show connections
4. **REFLECTION** - Pose thought-provoking questions within paragraphs
5. **LENGTH** - Write 800-1000 words

Write a comprehensive conclusion that:
- Summarizes the key concepts covered (in prose, not lists)
- Discusses how these concepts connect to broader research methodology
- Poses 10+ reflection questions for students (embedded in paragraphs, not as a list)
- Suggests practical exercises or applications (described in prose)
- Uses clear, academic language

Example of how to embed questions in prose:
"As students reflect on these concepts, they might consider how their own research context shapes their methodological choices. What ethical considerations arise when conducting research in post-conflict settings? How might limited resources influence the selection of data collection methods? These questions become particularly salient when..."

Use English ONLY. No non-English characters.

Write the summary now in flowing paragraphs:"""

    response = generator.generate(prompt, max_tokens=2500)
    return response
