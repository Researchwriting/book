from .llm import LLMClient
import json

class ChapterPlanner:
    def __init__(self):
        self.llm = LLMClient()

    def plan_chapter(self, chapter_key, chapter_title, topic, case_study):
        """
        Generate a custom outline for a specific chapter.
        """
        print(f"  Planning custom outline for {chapter_key}...")
        
        # Define chapter-specific planning instructions
        planning_instructions = {
            "CHAPTER ONE": """
                For Chapter 1 (Introduction), create a detailed outline that:
                - For "1.2 Background of the study": Use INVERTED PYRAMID structure (Global → Regional → Local)
                    - Global Context: International/worldwide perspective
                    - Regional Context: Continental or regional perspective
                    - Local Context: Country/case study specific
                - For other sections: Follow standard academic introduction format
                Return a JSON structure with section numbers as keys and sub-sections as arrays.
            """,
            "CHAPTER TWO": """
                For Chapter 2 (Literature Review), create a thematic outline:
                - Organize by 4 major themes related to the research objectives
                - Each theme should have clear arguments and counter-arguments
                - Include theoretical framework positioning
                Return a JSON structure with section numbers as keys and themes/arguments as arrays.
            """,
            "CHAPTER THREE": """
                For Chapter 3 (Methodology), create a structured research design outline:
                - Follow the logical flow: Philosophy → Design → Population → Sampling → Data Collection → Analysis
                - Be specific to the case study context
                Return a JSON structure with section numbers as keys and methodological steps as arrays.
            """,
            "CHAPTER FOUR": """
                For Chapter 4 (Data Presentation), create a results-oriented outline:
                - Organize by research questions/objectives
                - Each section should present findings for one research question
                - Include space for tables, charts, and descriptive statistics
                Return a JSON structure with section numbers as keys and research questions as arrays.
            """,
            "CHAPTER FIVE": """
                For Chapter 5 (Discussion), create an integrative outline:
                - Link findings (Ch 4) with literature (Ch 2)
                - Discuss implications and contributions
                - Address limitations
                Return a JSON structure with section numbers as keys and discussion points as arrays.
            """,
            "CHAPTER SIX": """
                For Chapter 6 (Conclusion), create a synthesis outline:
                - Summarize key findings
                - Draw conclusions aligned with objectives
                - Provide actionable recommendations
                Return a JSON structure with section numbers as keys and conclusion elements as arrays.
            """
        }
        
        instruction = planning_instructions.get(chapter_key, "Create a standard academic outline.")
        
        prompt = f"""
        You are planning a PhD thesis chapter for the University of Juba.
        
        TOPIC: {topic}
        CASE STUDY: {case_study}
        CHAPTER: {chapter_key} - {chapter_title}
        
        INSTRUCTIONS:
        {instruction}
        
        TASK:
        Generate a detailed, custom outline for this chapter. Return ONLY valid JSON in this format:
        {{
            "section_number": ["subsection 1", "subsection 2", ...],
            ...
        }}
        
        Example for Chapter 1, Background:
        {{
            "1.2 Background of the study": ["Global Context", "Regional Context", "Local Context"]
        }}
        
        Return ONLY the JSON, no other text.
        """
        
        try:
            response = self.llm.generate(prompt, system_prompt="You are an expert thesis advisor. Return only valid JSON.", max_tokens=2048)
            # Try to parse JSON
            outline = json.loads(response.strip())
            return outline
        except Exception as e:
            print(f"  Warning: Could not parse custom outline ({e}). Using default structure.")
            return {}
