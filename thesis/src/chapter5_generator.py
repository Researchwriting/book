"""
Chapter 5 Discussion Generator
Synthesizes findings from Chapter 4 with literature from Chapter 2
"""
from .llm import LLMClient
from .uk_english_compliance import UKEnglishCompliance

class Chapter5DiscussionGenerator:
    def __init__(self, llm_client, state_manager):
        self.llm = llm_client
        self.state_manager = state_manager
    
    def generate_chapter5(self, objectives, topic, case_study):
        """
        Generate complete Chapter 5: Results and Discussion
        
        Cross-references:
        - Chapter 4 findings
        - Chapter 2 literature (theories, studies, concepts)
        - Research objectives
        """
        print("\n📚 Generating Chapter 5: Results and Discussion...")
        
        # Retrieve context from previous chapters
        chapter2_content = self._get_chapter2_context()
        chapter4_findings = self._get_chapter4_findings()
        
        markdown = "# CHAPTER FIVE\n## RESULTS AND DISCUSSION\n\n"
        
        # 5.0 Introduction
        markdown += self._generate_introduction(objectives, topic, case_study)
        
        # 5.1+ Discussion per objective
        objectives_list = self._parse_objectives(objectives)
        
        for i, objective in enumerate(objectives_list, 1):
            markdown += self._generate_objective_discussion(
                objective_num=i,
                objective_text=objective,
                chapter2_content=chapter2_content,
                chapter4_findings=chapter4_findings,
                topic=topic,
                case_study=case_study
            )
        
        return markdown
    
    def _generate_introduction(self, objectives, topic, case_study):
        """Generate 5.0 Introduction"""
        print("  📝 Generating introduction...")
        
        prompt = f"""
Write the introduction for Chapter 5 (Results and Discussion) of a PhD thesis.

TOPIC: {topic}
CASE STUDY: {case_study}

OBJECTIVES:
{objectives}

REQUIREMENTS:
1. Explain the purpose of this chapter (synthesising findings with literature)
2. Briefly outline how findings from Chapter 4 will be discussed in relation to Chapter 2 literature
3. Mention that the chapter confirms or challenges existing knowledge
4. Explain the contribution of this study
5. Provide a brief chapter overview (one section per objective)

TENSE: Present tense for chapter purpose, future tense for what will be discussed
LENGTH: 400-600 words
UK ENGLISH: Use UK spelling (analyse, organisation, behaviour, etc.)
TONE: Academic, formal

{UKEnglishCompliance.get_system_prompt_suffix(5)}
"""
        
        intro = self.llm.generate(
            prompt,
            system_prompt="You are writing a PhD thesis chapter introduction.",
            max_tokens=800
        )
        
        intro = UKEnglishCompliance.convert_to_uk(intro)
        
        return f"## 5.0 Introduction\n\n{intro}\n\n"
    
    def _generate_objective_discussion(self, objective_num, objective_text, 
                                      chapter2_content, chapter4_findings, 
                                      topic, case_study):
        """
        Generate discussion for one objective.
        Cross-references Chapter 4 findings with Chapter 2 literature.
        """
        print(f"  💬 Generating discussion for Objective {objective_num}...")
        
        # Extract relevant literature from Chapter 2
        relevant_literature = self._extract_relevant_literature(
            objective_text, chapter2_content
        )
        
        # Extract relevant findings from Chapter 4
        relevant_findings = self._extract_relevant_findings(
            objective_num, chapter4_findings
        )
        
        prompt = f"""
Write the discussion section for Objective {objective_num} in Chapter 5 of a PhD thesis.

TOPIC: {topic}
CASE STUDY: {case_study}

OBJECTIVE {objective_num}:
{objective_text}

FINDINGS FROM CHAPTER 4:
{relevant_findings}

LITERATURE FROM CHAPTER 2:
{relevant_literature}

TASK: Write a comprehensive discussion that:

1. **Restates the objective** briefly
2. **Summarises key findings** from Chapter 4 related to this objective
3. **Cross-references with literature**:
   - Compare findings with previous studies (cite authors and years)
   - Discuss agreements with existing literature
   - Discuss contradictions or differences
   - Reference relevant theories and concepts
4. **Explains variations**:
   - Why findings confirm or differ from literature
   - Contextual factors (case study specific)
   - Methodological considerations
5. **Highlights contribution**:
   - What new knowledge this study adds
   - How it extends existing understanding

STRUCTURE:
### 5.{objective_num} Discussion of Objective {objective_num} Findings

[Introduction paragraph - restate objective and overview of findings]

[2-3 paragraphs - present findings and compare with literature]

[2-3 paragraphs - explain agreements/contradictions]

[1-2 paragraphs - discuss implications and contribution]

CRITICAL REQUIREMENTS:
- TENSE: Present tense for discussion ("The findings suggest...", "This confirms...")
- CROSS-REFERENCE: Explicitly cite Chapter 4 tables/figures ("As shown in Table 4.X...")
- CITE LITERATURE: Reference Chapter 2 studies ("This aligns with Smith (2020) who found...")
- UK ENGLISH: Use UK spelling throughout
- NO BULLETING: Use flowing academic prose
- LENGTH: 1500-2000 words per objective

{UKEnglishCompliance.get_system_prompt_suffix(5)}
"""
        
        discussion = self.llm.generate(
            prompt,
            system_prompt="You are writing a PhD thesis discussion section that synthesises findings with literature.",
            max_tokens=2500
        )
        
        discussion = UKEnglishCompliance.convert_to_uk(discussion)
        
        return discussion + "\n\n"
    
    def _get_chapter2_context(self):
        """Retrieve Chapter 2 content from state"""
        chapter2_sections = [
            "2.1 Introduction",
            "2.2 Theoretical Framework",
            "2.3 Empirical Literature",
            "2.4 Conceptual Framework",
            "2.5 Literature Gap"
        ]
        
        content = ""
        for section in chapter2_sections:
            section_content = self.state_manager.get_section_content("CHAPTER TWO", section)
            if section_content:
                content += f"\n### {section}\n{section_content}\n"
        
        return content if content else "Literature review content not available."
    
    def _get_chapter4_findings(self):
        """Retrieve Chapter 4 findings from state"""
        chapter4_sections = [
            "4.2 Demographic Characteristics",
            "4.3 Descriptive Statistics",
            "4.4 Correlation Analysis",
            "4.5 Regression Analysis",
            "4.6 Qualitative Findings"
        ]
        
        content = ""
        for section in chapter4_sections:
            section_content = self.state_manager.get_section_content("CHAPTER FOUR", section)
            if section_content:
                content += f"\n### {section}\n{section_content}\n"
        
        return content if content else "Chapter 4 findings not available."
    
    def _extract_relevant_literature(self, objective_text, chapter2_content):
        """Extract literature relevant to specific objective using LLM"""
        prompt = f"""
Extract literature from Chapter 2 that is relevant to this objective:

OBJECTIVE: {objective_text}

CHAPTER 2 CONTENT:
{chapter2_content[:3000]}...

TASK: Extract and summarise:
1. Relevant theories
2. Relevant empirical studies (with authors and years)
3. Relevant concepts
4. Key findings from previous research

Keep it concise (300-500 words).
"""
        
        relevant = self.llm.generate(
            prompt,
            system_prompt="You are extracting relevant literature for discussion.",
            max_tokens=600
        )
        
        return relevant
    
    def _extract_relevant_findings(self, objective_num, chapter4_findings):
        """Extract findings relevant to specific objective"""
        prompt = f"""
Extract findings from Chapter 4 that relate to Objective {objective_num}:

CHAPTER 4 FINDINGS:
{chapter4_findings[:3000]}...

TASK: Summarise:
1. Key statistical results (means, correlations, regression coefficients)
2. Qualitative themes and quotes
3. Tables and figures referenced
4. Main patterns observed

Keep it concise (300-500 words).
"""
        
        relevant = self.llm.generate(
            prompt,
            system_prompt="You are extracting relevant findings for discussion.",
            max_tokens=600
        )
        
        return relevant
    
    def _parse_objectives(self, objectives_text):
        """Parse objectives into a list"""
        # Simple parsing - extract numbered objectives
        import re
        
        # Look for patterns like "1. ", "i. ", "Objective 1:", etc.
        objectives = re.split(r'\n\s*(?:\d+\.|\([a-z]\)|\([ivx]+\))', objectives_text)
        objectives = [obj.strip() for obj in objectives if obj.strip() and len(obj.strip()) > 20]
        
        # If parsing fails, return as single objective
        if not objectives:
            objectives = [objectives_text]
        
        return objectives[:5]  # Max 5 objectives
