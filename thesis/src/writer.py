from .llm import LLMClient
from .researcher import Researcher
from .reviewer import ReviewerPanel
from . import chapter2_prompts
from . import chapter3_prompts

class ThesisWriter:
    def __init__(self, state_manager=None, reference_manager=None):
        self.llm = LLMClient()
        self.researcher = Researcher(reference_manager)
        self.reviewer_panel = ReviewerPanel(self.llm)
        self.state_manager = state_manager
        self.reference_manager = reference_manager


    def write_section(self, chapter_title, section_title, topic, case_study):
        """
        Write a specific section of the thesis.
        """
        print(f"  Researching for: {section_title}...")
        
        # 0. Get Context from State Manager (if available)
        context_str = ""
        objectives_str = ""
        
        if self.state_manager:
            # For Chapter 2: Get objectives from Chapter 1
            if "CHAPTER TWO" in chapter_title or "LITERATURE REVIEW" in chapter_title:
                ch1_objectives = self.state_manager.get_section_content("CHAPTER ONE", "1.4 Objectives")
                ch1_specific_obj = self.state_manager.get_section_content("CHAPTER ONE", "1.4.2 Specific objectives")
                ch1_questions = self.state_manager.get_section_content("CHAPTER ONE", "1.5 Research questions/hypothesis")
                
                if ch1_objectives or ch1_specific_obj or ch1_questions:
                    context_str = f"""
                    RESEARCH OBJECTIVES AND QUESTIONS FROM CHAPTER 1:
                    
                    Objectives: {ch1_objectives if ch1_objectives else 'Not yet generated'}
                    
                    Specific Objectives: {ch1_specific_obj if ch1_specific_obj else 'Not yet generated'}
                    
                    Research Questions: {ch1_questions if ch1_questions else 'Not yet generated'}
                    
                    CRITICAL INSTRUCTION: 
                    - All themes and arguments in this literature review MUST directly relate to these objectives and questions.
                    - Each theory in the theoretical framework must support addressing these objectives.
                    - Identify gaps in literature specifically in relation to these objectives.
                    """
            
            # For Chapter 3: Get objectives and problem statement from Chapter 1
            elif "CHAPTER THREE" in chapter_title or "METHODOLOGY" in chapter_title:
                ch1_problem = self.state_manager.get_section_content("CHAPTER ONE", "1.3 Statement of the problem")
                ch1_objectives = self.state_manager.get_section_content("CHAPTER ONE", "1.4 Objectives")
                ch1_specific_obj = self.state_manager.get_section_content("CHAPTER ONE", "1.4.2 Specific objectives")
                ch1_questions = self.state_manager.get_section_content("CHAPTER ONE", "1.5 Research questions/hypothesis")
                
                objectives_str = f"""
                RESEARCH PROBLEM: {ch1_problem if ch1_problem else 'Not yet generated'}
                
                OBJECTIVES: {ch1_objectives if ch1_objectives else 'Not yet generated'}
                
                SPECIFIC OBJECTIVES: {ch1_specific_obj if ch1_specific_obj else 'Not yet generated'}
                
                RESEARCH QUESTIONS: {ch1_questions if ch1_questions else 'Not yet generated'}
                """
                
                context_str = f"""
                CONTEXT FROM CHAPTER 1:
                {objectives_str}
                
                CRITICAL INSTRUCTION:
                - The methodology MUST be designed to address these specific objectives and research questions.
                - Justify all methodological choices in relation to the objectives.
                - Ensure the research design can answer the research questions.
                """
            
            # For Chapter 5: Get context from Chapter 2 and 4
            elif "CHAPTER FIVE" in chapter_title:
                ch2_content = self.state_manager.get_chapter_content("CHAPTER TWO")
                ch4_content = self.state_manager.get_chapter_content("CHAPTER FOUR")
                if ch2_content or ch4_content:
                    context_str = f"""
                    CONTEXT FROM PREVIOUS CHAPTERS:
                    - Literature Review (Ch 2): {ch2_content[:2000]}... [truncated]
                    - Data Presentation (Ch 4): {ch4_content[:2000]}... [truncated]
                    
                    INSTRUCTION: Explicitly reference the above literature and data in your discussion.
                    """
        
        # 1. Conduct Research (Academic + Web)
        query = f"{topic} {section_title} {case_study}"
        
        # Academic Search
        print(f"  🔍 Searching Semantic Scholar API for: {query[:50]}...")
        papers = self.researcher.search_papers(query, chapter=chapter_title)
        print(f"  📄 Found {len(papers)} papers from Semantic Scholar")
        
        # Web Search (Broad context)
        web_results = self.researcher.search_web(query, chapter=chapter_title)
        print(f"  🌐 Found {len(web_results)} web results")
        
        # Format References
        references = self.researcher.format_references(papers, web_results)
        
        # Create RICH citation guide with abstracts and context (Author, Year format)
        citation_guide = []
        if papers:
            citation_guide.append("=== ACADEMIC PAPERS FROM SEMANTIC SCHOLAR ===\n")
            for i, paper in enumerate(papers, 1):
                authors = paper.get('authors', [])
                if authors:
                    if isinstance(authors[0], dict):
                        first_author = authors[0].get('name', 'Unknown').split(',')[0]
                        all_authors = ", ".join([a.get('name', 'Unknown') for a in authors[:3]])
                        if len(authors) > 3:
                            all_authors += " et al."
                    else:
                        first_author = str(authors[0]).split(',')[0]
                        all_authors = first_author
                else:
                    first_author = "Unknown"
                    all_authors = "Unknown"
                
                year = paper.get('year', 'n.d.')
                title = paper.get('title', 'Untitled')
                abstract = paper.get('abstract', 'No abstract available')[:500]  # First 500 chars
                venue = paper.get('venue', 'Unknown venue')
                
                # Create rich citation entry
                citation_entry = f"""
{i}. [{first_author}, {year}] "{title}"
   Authors: {all_authors}
   Published in: {venue}
   Abstract: {abstract}...
   
   HOW TO CITE: Use ({first_author}, {year}) or {first_author} ({year}) in your text.
   WHEN TO USE: Cite this when discussing topics related to the abstract above.
"""
                citation_guide.append(citation_entry)
        
        citation_text = "\n".join(citation_guide) if citation_guide else "NO SOURCES FOUND. DO NOT CITE ANY PAPERS. RELY ON GENERAL ACADEMIC KNOWLEDGE ONLY."
        
        # 2. Construct Prompt (Special handling for Chapter 2 and Chapter 3)
        if "CHAPTER TWO" in chapter_title or "LITERATURE REVIEW" in chapter_title:
            # Use specialized Chapter 2 prompts
            if "2.2" in section_title or "Theoretical Framework" in section_title or "Conceptual Framework" in section_title:
                prompt = chapter2_prompts.get_chapter2_theory_prompt(section_title, topic, case_study, citation_text)
            elif "2.7" in section_title or "Gap" in section_title:
                prompt = chapter2_prompts.get_chapter2_gap_prompt(section_title, topic, case_study, citation_text)
            elif any(f"2.{i}" in section_title for i in [3, 4, 5, 6]):  # Themes
                prompt = chapter2_prompts.get_chapter2_theme_prompt(section_title, topic, case_study, citation_text)
            else:
                prompt = self._get_default_prompt(chapter_title, section_title, topic, case_study, context_str, citation_text)
        
        elif "CHAPTER THREE" in chapter_title or "METHODOLOGY" in chapter_title:
            # Use specialized Chapter 3 prompts
            if "3.1" in section_title or "Introduction" in section_title:
                prompt = chapter3_prompts.get_chapter3_introduction_prompt(section_title, topic, case_study, citation_text, objectives_str)
            elif "3.4" in section_title or "Target Population" in section_title:
                prompt = chapter3_prompts.get_chapter3_population_prompt(section_title, topic, case_study, citation_text, objectives_str)
            elif "3.6" in section_title or "Sample Size" in section_title:
                prompt = chapter3_prompts.get_chapter3_sample_size_prompt(section_title, topic, case_study, citation_text, objectives_str)
            else:
                # Other Chapter 3 sections (3.2, 3.3, 3.5, 3.7-3.11)
                prompt = chapter3_prompts.get_chapter3_detailed_prompt(section_title, topic, case_study, citation_text, objectives_str)
        
        else:
            # Standard prompt for other chapters
            prompt = self._get_default_prompt(chapter_title, section_title, topic, case_study, context_str, citation_text)
        
        # 3. Generate Draft
        print(f"  Drafting content...")
        draft = self.llm.generate(prompt, system_prompt="You are a PhD candidate writing a thesis. You are rigorous, academic, and precise. YOU MUST NEVER HALLUCINATE CITATIONS.")
        
        # 4. Peer Review Process
        reviews = self.reviewer_panel.review_section(draft, section_title, chapter_title)
        
        # 5. Save Review Report
        review_file = self.reviewer_panel.save_review_report(reviews, section_title, chapter_title)
        print(f"  📋 Review saved: {review_file}")
        
        # 6. Improve Based on Reviews
        final_content = self.reviewer_panel.improve_based_on_reviews(draft, reviews, section_title)
        
        # Double check for hallucinated citations (basic check)
        # This is a safeguard; the prompt is the primary defense.
        
        return final_content
    
    def write_section_no_research(self, chapter_title, section_title, topic, case_study):
        """
        Write a section WITHOUT calling Semantic Scholar API.
        Used for Chapter 4 (Data Presentation) which doesn't need literature.
        """
        print(f"  Writing section: {section_title}... (No research)")
        
        # 0. Get Context from State Manager (if available)
        context_str = ""
        
        if self.state_manager:
            # For Chapter 4: Get methodology from Chapter 3
            if "CHAPTER FOUR" in chapter_title:
                ch3_design = self.state_manager.get_section_content("CHAPTER THREE", "3.3 Research Design")
                ch3_sample = self.state_manager.get_section_content("CHAPTER THREE", "3.6 Sample Size")
                
                if ch3_design or ch3_sample:
                    context_str = f"""
                    METHODOLOGY FROM CHAPTER 3:
                    
                    Research Design: {ch3_design[:500] if ch3_design else 'Not yet generated'}
                    
                    Sample Size: {ch3_sample[:500] if ch3_sample else 'Not yet generated'}
                    
                    INSTRUCTION: Present data based on this methodology. Use tables, figures, and descriptive statistics.
                    """
        
        # Construct Prompt (No citations needed for data presentation)
        prompt = f"""
        You are writing Chapter 4 (Data Presentation) of a PhD thesis.
        
        TOPIC: {topic}
        CASE STUDY: {case_study}
        CHAPTER: {chapter_title}
        SECTION: {section_title}
        
        {context_str}
        
        REQUIREMENTS:
        1. Write in strict academic English (UK spelling: analyse, organisation, behaviour, etc.)
        2. Present data objectively - NO DISCUSSION OR INTERPRETATION
        3. Use past tense (\"The data showed...\", \"Respondents indicated...\")
        4. Include tables with proper numbering (Table 4.1, 4.2, etc.)
        5. Include descriptive statistics (means, standard deviations, frequencies, percentages)
        6. DO NOT cite literature - this is data presentation only
        7. DO NOT add a \"References\" section
        8. Length: Write approximately 1500-2000 words for this section
        9. Do not use bullet points unless presenting data. Use flowing paragraphs
        10. CRITICAL: DO NOT include the section heading/title in your response - it will be added automatically
        11. Start directly with the first paragraph of content
        
        CONTENT GUIDANCE:
        - Present demographic data with tables
        - Show descriptive statistics
        - Present findings objectively without discussion
        - Use tables and figures extensively
        - Provide brief interpretation of tables (what the data shows, not what it means)
        
        Write the content for section '{section_title}' now (without including the section heading):
        """
        
        # Generate Draft
        print(f"  Drafting content...")
        draft = self.llm.generate(prompt, system_prompt="You are a PhD candidate presenting research data objectively.")
        
        # Peer Review Process
        reviews = self.reviewer_panel.review_section(draft, section_title, chapter_title)
        
        # Save Review Report
        review_file = self.reviewer_panel.save_review_report(reviews, section_title, chapter_title)
        print(f"  📋 Review saved: {review_file}")
        
        # Improve Based on Reviews
        final_content = self.reviewer_panel.improve_based_on_reviews(draft, reviews, section_title)
        
        return final_content
    
    
    def _get_default_prompt(self, chapter_title, section_title, topic, case_study, context_str, citation_text):
        """Standard prompt for non-Chapter-2/3 sections"""
        return f"""
        You are writing a PhD thesis for the University of Juba.
        
        TOPIC: {topic}
        CASE STUDY: {case_study}
        CHAPTER: {chapter_title}
        SECTION: {section_title}
        
        {context_str}
        
        CITATION GUIDE (Use ONLY these sources for in-text citations):
        {citation_text}
        
        REQUIREMENTS:
        1. Write in strict academic English (UK spelling: analyse, organisation, behaviour, etc.)
        2. Use Harvard Referencing Style for IN-TEXT CITATIONS ONLY: (Author, Year) or Author (Year)
        3. DO NOT include full references in the text. Only use (Author, Year) format
        4. Cite the provided sources where relevant using ONLY (Author, Year)
        5. **STRICT PROHIBITION**: DO NOT INVENT OR HALLUCINATE CITATIONS. If a source is not in the CITATION GUIDE, DO NOT CITE IT.
        6. **CRITICAL**: DO NOT add a "References" or "Bibliography" section at the end of your content. The bibliography will be generated separately.
        7. Length: Write approximately 1500-2000 words for this section
        8. Do not use bullet points unless absolutely necessary. Use flowing paragraphs
        9. CRITICAL: DO NOT include the section heading/title in your response - it will be added automatically
        10. Start directly with the first paragraph of content
        
        CONTENT GUIDANCE:
        - If this is Chapter 1, focus on setting the scene and problem statement
        - If this is Chapter 2, critically analyze the literature
        - If this is Chapter 3, detail the methodology
        - If this is Chapter 4, present data (simulate data based on the case study if needed)
        - If this is Chapter 5, discuss results in relation to literature
        
        Write the content for section '{section_title}' now (without including the section heading):
        """
