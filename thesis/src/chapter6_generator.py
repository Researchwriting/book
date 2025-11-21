"""
Chapter 6 Generator
Summary, Conclusion and Recommendation
Synthesizes all previous chapters (1-5)
"""
from .llm import LLMClient
from .uk_english_compliance import UKEnglishCompliance

class Chapter6Generator:
    def __init__(self, llm_client, state_manager):
        self.llm = llm_client
        self.state_manager = state_manager
    
    def generate_chapter6(self, objectives, topic, case_study):
        """
        Generate complete Chapter 6: Summary, Conclusion and Recommendation
        
        Synthesizes:
        - Chapter 1: Problem, objectives, questions
        - Chapter 2: Literature gaps
        - Chapter 3: Methodology
        - Chapter 4: Findings
        - Chapter 5: Discussion
        """
        print("\n📝 Generating Chapter 6: Summary, Conclusion and Recommendation...")
        
        # Retrieve context from all previous chapters
        chapter_summaries = self._get_all_chapter_summaries()
        
        markdown = "# CHAPTER SIX\n## SUMMARY, CONCLUSION AND RECOMMENDATION\n\n"
        
        # 6.1 Summary
        markdown += self._generate_summary(
            objectives, topic, case_study, chapter_summaries
        )
        
        # 6.2 Conclusion
        markdown += self._generate_conclusion(
            objectives, topic, case_study, chapter_summaries
        )
        
        # 6.3 Recommendation
        markdown += self._generate_recommendations(
            objectives, topic, case_study, chapter_summaries
        )
        
        # 6.4 Suggestions for Future Research
        markdown += self._generate_future_research(
            objectives, topic, case_study, chapter_summaries
        )
        
        return markdown
    
    def _generate_summary(self, objectives, topic, case_study, chapter_summaries):
        """Generate 6.1 Summary"""
        print("  📋 Generating summary...")
        
        prompt = f"""
Write Section 6.1 (Summary) for Chapter 6 of a PhD thesis.

TOPIC: {topic}
CASE STUDY: {case_study}

OBJECTIVES:
{objectives}

CHAPTER SUMMARIES:
{chapter_summaries}

TASK: Write a comprehensive summary that:

1. **Restates the research problem** (from Chapter 1)
2. **Summarises the objectives** (from Chapter 1)
3. **Summarises the methodology** (from Chapter 3):
   - Research design
   - Sample size
   - Data collection methods
   - Analysis techniques
4. **Summarises key findings** (from Chapter 4):
   - Main statistical results
   - Key qualitative themes
   - Important patterns observed
5. **Summarises main discussion points** (from Chapter 5):
   - How findings relate to literature
   - Key contributions

STRUCTURE:
## 6.1 Summary

[Paragraph 1: Problem and objectives]
[Paragraph 2: Methodology overview]
[Paragraph 3-4: Key findings per objective]
[Paragraph 5: Main discussion points]

REQUIREMENTS:
- TENSE: Past tense ("The study examined...", "Data were collected...", "The findings revealed...")
- LENGTH: 800-1200 words
- UK ENGLISH: analyse, organisation, behaviour, etc.
- NO BULLETING: Flowing prose
- COMPREHENSIVE: Cover all chapters 1-5

{UKEnglishCompliance.get_system_prompt_suffix(6)}
"""
        
        summary = self.llm.generate(
            prompt,
            system_prompt="You are writing a PhD thesis summary that synthesises all previous chapters.",
            max_tokens=1500
        )
        
        summary = UKEnglishCompliance.convert_to_uk(summary)
        
        return summary + "\n\n"
    
    def _generate_conclusion(self, objectives, topic, case_study, chapter_summaries):
        """Generate 6.2 Conclusion"""
        print("  ✅ Generating conclusion...")
        
        prompt = f"""
Write Section 6.2 (Conclusion) for Chapter 6 of a PhD thesis.

TOPIC: {topic}
CASE STUDY: {case_study}

OBJECTIVES:
{objectives}

CHAPTER SUMMARIES:
{chapter_summaries}

TASK: Write conclusions that:

1. **Restate the research problem and objectives** briefly
2. **Present conclusions per objective**:
   - One conclusion statement per objective
   - Based on findings and discussion
   - Clear, definitive statements
3. **Overall conclusion**:
   - What the study has demonstrated
   - Contribution to knowledge
   - Implications for theory and practice

STRUCTURE:
## 6.2 Conclusion

[Paragraph 1: Restate problem and objectives]

[Paragraph 2: Conclusion for Objective 1]
Based on the findings and discussion, the study concludes that...

[Paragraph 3: Conclusion for Objective 2]
The study further concludes that...

[Continue for all objectives]

[Final paragraph: Overall conclusion and contribution]

REQUIREMENTS:
- TENSE: Present tense for conclusions ("The study concludes...", "This demonstrates...", "The evidence suggests...")
- LENGTH: 600-1000 words
- UK ENGLISH: analyse, organisation, behaviour, etc.
- NO BULLETING: Flowing prose
- DEFINITIVE: Clear, confident conclusion statements
- EVIDENCE-BASED: Grounded in findings

{UKEnglishCompliance.get_system_prompt_suffix(6)}
"""
        
        conclusion = self.llm.generate(
            prompt,
            system_prompt="You are writing PhD thesis conclusions based on research findings.",
            max_tokens=1200
        )
        
        conclusion = UKEnglishCompliance.convert_to_uk(conclusion)
        
        return conclusion + "\n\n"
    
    def _generate_recommendations(self, objectives, topic, case_study, chapter_summaries):
        """Generate 6.3 Recommendation"""
        print("  💡 Generating recommendations...")
        
        prompt = f"""
Write Section 6.3 (Recommendation) for Chapter 6 of a PhD thesis.

TOPIC: {topic}
CASE STUDY: {case_study}

OBJECTIVES:
{objectives}

CHAPTER SUMMARIES:
{chapter_summaries}

TASK: Write practical recommendations that:

1. **Are based on findings and conclusions**
2. **Are actionable and specific**
3. **Target different stakeholders**:
   - Government/policymakers
   - Practitioners/organisations
   - Community/local actors
   - Researchers
4. **Link to objectives**

STRUCTURE:
## 6.3 Recommendation

[Introduction paragraph: Purpose of recommendations]

### 6.3.1 Recommendations for Government/Policymakers
Based on the findings that [reference finding], it is recommended that...
[3-5 specific recommendations]

### 6.3.2 Recommendations for Practitioners/Organisations
The study recommends that...
[3-5 specific recommendations]

### 6.3.3 Recommendations for Community/Local Actors
It is recommended that...
[2-3 specific recommendations]

### 6.3.4 Recommendations for Researchers
[2-3 specific recommendations]

REQUIREMENTS:
- TENSE: Present tense ("It is recommended...", "The study recommends...", "Stakeholders should...")
- LENGTH: 1000-1500 words
- UK ENGLISH: analyse, organisation, behaviour, etc.
- NO BULLETING: Use subsections with flowing prose
- SPECIFIC: Concrete, actionable recommendations
- EVIDENCE-BASED: Link to findings

Example:
"Based on the finding that war exposure significantly increases unemployment (r = 0.67, p < 0.001), it is recommended that the government establishes targeted employment programmes for conflict-affected populations. These programmes should focus on skills training, job placement services, and entrepreneurship support to facilitate economic reintegration..."

{UKEnglishCompliance.get_system_prompt_suffix(6)}
"""
        
        recommendations = self.llm.generate(
            prompt,
            system_prompt="You are writing practical, evidence-based recommendations for a PhD thesis.",
            max_tokens=1800
        )
        
        recommendations = UKEnglishCompliance.convert_to_uk(recommendations)
        
        return recommendations + "\n\n"
    
    def _generate_future_research(self, objectives, topic, case_study, chapter_summaries):
        """Generate 6.4 Suggestions for Future Research"""
        print("  🔬 Generating future research suggestions...")
        
        prompt = f"""
Write Section 6.4 (Suggestions for Future Research) for Chapter 6 of a PhD thesis.

TOPIC: {topic}
CASE STUDY: {case_study}

OBJECTIVES:
{objectives}

CHAPTER SUMMARIES:
{chapter_summaries}

TASK: Suggest future research directions that:

1. **Address limitations of current study**
2. **Extend the research to new contexts**
3. **Explore related phenomena**
4. **Use different methodologies**
5. **Investigate emerging issues**

STRUCTURE:
## 6.4 Suggestions for Future Research

[Introduction paragraph: Importance of future research]

[Paragraph 1: Suggestion 1]
Future research could explore...
This would extend understanding by...

[Paragraph 2: Suggestion 2]
Researchers may investigate...
This would address the limitation of...

[Paragraph 3: Suggestion 3]
A longitudinal study examining...
This would provide insights into...

[Continue for 5-7 suggestions]

[Concluding paragraph: Overall research agenda]

REQUIREMENTS:
- TENSE: Present/Future ("Future research could...", "Researchers may...", "Studies should...")
- LENGTH: 600-800 words
- UK ENGLISH: analyse, organisation, behaviour, etc.
- NO BULLETING: Flowing prose
- SPECIFIC: Concrete research questions/directions
- JUSTIFIED: Explain why each suggestion is important

Example:
"Future research could explore the long-term effects of war on employment patterns by conducting a longitudinal study over 10-15 years. This would address the limitation of the current cross-sectional design and provide insights into how employment trajectories evolve as post-conflict recovery progresses. Such research would be particularly valuable for informing sustainable development policies in conflict-affected regions..."

{UKEnglishCompliance.get_system_prompt_suffix(6)}
"""
        
        future_research = self.llm.generate(
            prompt,
            system_prompt="You are suggesting future research directions for a PhD thesis.",
            max_tokens=1000
        )
        
        future_research = UKEnglishCompliance.convert_to_uk(future_research)
        
        return future_research + "\n\n"
    
    def _get_all_chapter_summaries(self):
        """Retrieve summaries from all previous chapters"""
        summaries = ""
        
        # Chapter 1
        ch1_sections = ["1.3 Statement of the problem", "1.4 Objectives", "1.5 Research questions/hypothesis"]
        summaries += "\n### CHAPTER 1 - INTRODUCTION\n"
        for section in ch1_sections:
            content = self.state_manager.get_section_content("CHAPTER ONE", section)
            if content:
                summaries += f"{section}:\n{content[:500]}...\n\n"
        
        # Chapter 2
        summaries += "\n### CHAPTER 2 - LITERATURE REVIEW\n"
        ch2_content = self.state_manager.get_section_content("CHAPTER TWO", "2.5 Literature Gap")
        if ch2_content:
            summaries += f"Key gaps identified:\n{ch2_content[:500]}...\n\n"
        
        # Chapter 3
        summaries += "\n### CHAPTER 3 - METHODOLOGY\n"
        ch3_sections = ["3.3 Research Design", "3.6 Sample Size"]
        for section in ch3_sections:
            content = self.state_manager.get_section_content("CHAPTER THREE", section)
            if content:
                summaries += f"{section}:\n{content[:300]}...\n\n"
        
        # Chapter 4
        summaries += "\n### CHAPTER 4 - DATA PRESENTATION\n"
        ch4_content = self.state_manager.get_section_content("CHAPTER FOUR", "4.3 Descriptive Statistics")
        if ch4_content:
            summaries += f"Key findings:\n{ch4_content[:500]}...\n\n"
        
        # Chapter 5
        summaries += "\n### CHAPTER 5 - DISCUSSION\n"
        ch5_content = self.state_manager.get_section_content("CHAPTER FIVE", "5.1 Discussion of Objective 1 Findings")
        if ch5_content:
            summaries += f"Main discussion points:\n{ch5_content[:500]}...\n\n"
        
        return summaries if summaries else "Previous chapter content not available."
