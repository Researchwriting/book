"""
Chapter 4 Analysis Planner
Determines appropriate analyses based on objectives, methodology, and data
"""
from .llm import LLMClient

class Chapter4Planner:
    def __init__(self, llm_client):
        self.llm = llm_client
    
    def plan_chapter4_analysis(self, objectives, methodology, dataset_info, research_questions):
        """
        Plan Chapter 4 structure and analyses based on research design.
        
        Args:
            objectives: Research objectives from Chapter 1
            methodology: Methodology description from Chapter 3
            dataset_info: Info about the dataset (columns, types, size)
            research_questions: Research questions from Chapter 1
        
        Returns:
            Dictionary with chapter outline and analysis plan
        """
        print("\n📋 Planning Chapter 4 structure and analyses...")
        
        prompt = f"""
You are planning the data analysis chapter (Chapter 4) for a PhD thesis.

RESEARCH OBJECTIVES:
{objectives}

RESEARCH QUESTIONS:
{research_questions}

METHODOLOGY:
{methodology}

DATASET INFORMATION:
{dataset_info}

TASK: Create a detailed analysis plan for Chapter 4 that includes:

1. **Chapter 4 Outline**: Sections and subsections
2. **Analysis Strategy**: Which statistical/qualitative analyses to perform
3. **Analysis-to-Objective Mapping**: Link each analysis to specific objectives

OUTPUT FORMAT (JSON):
{{
    "chapter_outline": {{
        "4.1": "Introduction",
        "4.2": "Demographic Characteristics",
        "4.3": "Descriptive Statistics",
        "4.4": "[Analysis based on objectives]",
        "4.5": "[Analysis based on objectives]",
        ...
    }},
    "quantitative_analyses": [
        {{
            "analysis_type": "correlation|regression|anova|t-test|chi-square|factor_analysis|mediation|moderation|panel|time_series",
            "variables": ["var1", "var2"],
            "objective": "Which objective this addresses",
            "rationale": "Why this analysis is appropriate"
        }}
    ],
    "qualitative_analyses": [
        {{
            "analysis_type": "thematic|content|document|narrative|discourse",
            "data_source": "interview_column|theme_column",
            "objective": "Which objective this addresses",
            "rationale": "Why this analysis is appropriate"
        }}
    ],
    "visualizations": [
        {{
            "type": "bar_chart|pie_chart|histogram|heatmap|grouped_bar",
            "data": "What to visualize",
            "purpose": "Why this visualization"
        }}
    ]
}}

GUIDELINES:
- Choose analyses that directly address the research objectives
- Match analysis type to methodology (quantitative/qualitative/mixed)
- Ensure statistical power and appropriateness
- Include both descriptive and inferential analyses
- Plan visualizations that enhance understanding

Return ONLY valid JSON.
"""
        
        response = self.llm.generate(
            prompt,
            system_prompt="You are a research methodology expert planning data analysis.",
            max_tokens=3000
        )
        
        # Parse JSON response
        import json
        try:
            analysis_plan = json.loads(response)
        except:
            # Fallback to default plan
            analysis_plan = self._get_default_plan()
        
        print(f"  ✅ Planned {len(analysis_plan.get('quantitative_analyses', []))} quantitative analyses")
        print(f"  ✅ Planned {len(analysis_plan.get('qualitative_analyses', []))} qualitative analyses")
        print(f"  ✅ Planned {len(analysis_plan.get('visualizations', []))} visualizations")
        
        return analysis_plan
    
    def _get_default_plan(self):
        """Default analysis plan if LLM fails"""
        return {
            "chapter_outline": {
                "4.1": "Introduction",
                "4.2": "Demographic Characteristics",
                "4.3": "Descriptive Statistics",
                "4.4": "Correlation Analysis",
                "4.5": "Regression Analysis",
                "4.6": "Qualitative Findings"
            },
            "quantitative_analyses": [
                {
                    "analysis_type": "correlation",
                    "variables": ["all_numeric"],
                    "objective": "Explore relationships",
                    "rationale": "Identify significant correlations"
                },
                {
                    "analysis_type": "regression",
                    "variables": ["dependent", "independents"],
                    "objective": "Test predictive relationships",
                    "rationale": "Determine predictors"
                }
            ],
            "qualitative_analyses": [
                {
                    "analysis_type": "thematic",
                    "data_source": "interview_responses",
                    "objective": "Understand experiences",
                    "rationale": "Extract themes from narratives"
                }
            ],
            "visualizations": [
                {"type": "bar_chart", "data": "demographics", "purpose": "Show distribution"},
                {"type": "heatmap", "data": "correlations", "purpose": "Visualize relationships"}
            ]
        }
    
    def generate_chapter4_outline_markdown(self, analysis_plan):
        """Generate markdown outline for Chapter 4"""
        markdown = "# CHAPTER FOUR: DATA PRESENTATION AND ANALYSIS\n\n"
        markdown += "## Chapter Outline\n\n"
        
        for section, title in analysis_plan['chapter_outline'].items():
            markdown += f"### {section} {title}\n"
        
        markdown += "\n## Planned Analyses\n\n"
        
        # Quantitative
        if analysis_plan.get('quantitative_analyses'):
            markdown += "### Quantitative Analyses\n\n"
            for i, analysis in enumerate(analysis_plan['quantitative_analyses'], 1):
                markdown += f"{i}. **{analysis['analysis_type'].upper()}**\n"
                markdown += f"   - Variables: {', '.join(analysis.get('variables', []))}\n"
                markdown += f"   - Objective: {analysis['objective']}\n"
                markdown += f"   - Rationale: {analysis['rationale']}\n\n"
        
        # Qualitative
        if analysis_plan.get('qualitative_analyses'):
            markdown += "### Qualitative Analyses\n\n"
            for i, analysis in enumerate(analysis_plan['qualitative_analyses'], 1):
                markdown += f"{i}. **{analysis['analysis_type'].upper()}**\n"
                markdown += f"   - Data Source: {analysis.get('data_source', 'N/A')}\n"
                markdown += f"   - Objective: {analysis['objective']}\n"
                markdown += f"   - Rationale: {analysis['rationale']}\n\n"
        
        return markdown
    
    def save_analysis_plan(self, analysis_plan, output_dir="thesis/output"):
        """Save the analysis plan"""
        import os
        import json
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Save JSON
        json_file = f"{output_dir}/Chapter4_Analysis_Plan.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_plan, f, indent=2)
        
        # Save markdown outline
        markdown = self.generate_chapter4_outline_markdown(analysis_plan)
        md_file = f"{output_dir}/Chapter4_Outline.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(markdown)
        
        print(f"  ✅ Analysis plan saved: {json_file}")
        print(f"  ✅ Outline saved: {md_file}")
        
        return json_file, md_file
