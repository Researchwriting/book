"""
Data Analysis Orchestrator
Coordinates quantitative and qualitative analysis for Chapter 4
"""
from .quantitative_analyzer import QuantitativeAnalyzer
from .qualitative_analyzer import QualitativeAnalyzer
from .visualization_generator import VisualizationGenerator
import os

class DataAnalysisOrchestrator:
    def __init__(self, data_dir="thesis/data", planner=None):
        self.data_dir = data_dir
        self.viz_gen = VisualizationGenerator()
        self.planner = planner  # Chapter4Planner instance
        
    def analyze_all_data(self, objectives="", methodology="", research_questions=""):
        """
        Perform complete data analysis for Chapter 4.
        Uses planner to determine appropriate analyses.
        Returns markdown content with tables, statistics, and visualizations.
        """
        print("\n📊 Starting comprehensive data analysis...")
        
        # Get dataset info
        dataset_info = self._get_dataset_info()
        
        # Plan analyses if planner is available
        if self.planner:
            analysis_plan = self.planner.plan_chapter4_analysis(
                objectives=objectives,
                methodology=methodology,
                dataset_info=dataset_info,
                research_questions=research_questions
            )
            self.planner.save_analysis_plan(analysis_plan)
        else:
            analysis_plan = None
        
        # Don't add chapter heading here - it will be added by thesis_main.py
        markdown_content = ""
        markdown_content += "## 4.1 Introduction\n\n"
        markdown_content += "This chapter presents and analyses the data collected through the research instruments described in Chapter 3. "
        markdown_content += "The analysis addresses each research objective systematically.\n\n"
        
        # Check for quantitative data
        quant_file = f"{self.data_dir}/Quantitative_Data.csv"
        if os.path.exists(quant_file):
            markdown_content += self._analyze_quantitative_data(quant_file, objectives, analysis_plan)
        
        # Check for qualitative data
        qual_file = f"{self.data_dir}/Qualitative_Data.csv"
        if os.path.exists(qual_file):
            markdown_content += self._analyze_qualitative_data(qual_file, objectives, analysis_plan)
        
        return markdown_content
    
    def _get_dataset_info(self):
        """Get information about available datasets"""
        import pandas as pd
        
        info = {"quantitative": None, "qualitative": None}
        
        quant_file = f"{self.data_dir}/Quantitative_Data.csv"
        if os.path.exists(quant_file):
            df = pd.read_csv(quant_file)
            info["quantitative"] = {
                "rows": len(df),
                "columns": df.columns.tolist(),
                "numeric_vars": df.select_dtypes(include=['int64', 'float64']).columns.tolist(),
                "categorical_vars": df.select_dtypes(include=['object']).columns.tolist()
            }
        
        qual_file = f"{self.data_dir}/Qualitative_Data.csv"
        if os.path.exists(qual_file):
            df = pd.read_csv(qual_file)
            info["qualitative"] = {
                "participants": len(df),
                "columns": df.columns.tolist()
            }
        
        return info
    
    def _analyze_quantitative_data(self, csv_file, objectives, analysis_plan=None):
        """Analyze quantitative data"""
        print("\n📊 Analyzing quantitative data...")
        
        analyzer = QuantitativeAnalyzer(csv_file)
        markdown = ""
        
        # Demographics
        markdown += "## 4.2 Demographic Characteristics of Respondents\n\n"
        demographics = analyzer.get_demographics_summary()
        
        # Gender distribution
        if 'gender' in demographics:
            markdown += "### 4.2.1 Gender Distribution\n\n"
            gender_data = demographics['gender']
            total = sum(gender_data.values())
            
            markdown += "**Table 4.1:** Gender Distribution of Respondents\n\n"
            markdown += "| Gender | Frequency | Percentage (%) |\n"
            markdown += "|--------|-----------|----------------|\n"
            for gender, count in gender_data.items():
                pct = (count / total * 100)
                markdown += f"| {gender} | {count} | {pct:.1f} |\n"
            markdown += f"| **Total** | **{total}** | **100.0** |\n\n"
            
            # Create visualization
            viz_file = self.viz_gen.create_pie_chart(
                gender_data,
                "Gender Distribution of Respondents",
                "gender_distribution.png"
            )
            markdown += f"![Gender Distribution]({viz_file})\n\n"
            markdown += f"**Figure 4.1:** Gender Distribution of Respondents\n\n"
            
            # Interpretation
            markdown += "The data shows that "
            for gender, count in gender_data.items():
                pct = (count / total * 100)
                markdown += f"{pct:.1f}% of respondents were {gender.lower()}, "
            markdown += f"indicating a {'balanced' if abs(list(gender_data.values())[0] - list(gender_data.values())[1]) < total * 0.1 else 'slightly imbalanced'} gender representation in the sample.\n\n"
        
        # Education distribution
        if 'education' in demographics:
            markdown += "### 4.2.2 Education Level Distribution\n\n"
            edu_data = demographics['education']
            total = sum(edu_data.values())
            
            markdown += "**Table 4.2:** Education Level Distribution\n\n"
            markdown += "| Education Level | Frequency | Percentage (%) |\n"
            markdown += "|----------------|-----------|----------------|\n"
            for edu, count in edu_data.items():
                pct = (count / total * 100)
                markdown += f"| {edu} | {count} | {pct:.1f} |\n"
            markdown += f"| **Total** | **{total}** | **100.0** |\n\n"
            
            # Create visualization
            viz_file = self.viz_gen.create_bar_chart(
                edu_data,
                "Education Level Distribution",
                "Education Level",
                "Frequency",
                "education_distribution.png"
            )
            markdown += f"![Education Distribution]({viz_file})\n\n"
            markdown += f"**Figure 4.2:** Education Level Distribution\n\n"
        
        # Descriptive statistics
        markdown += "## 4.3 Descriptive Statistics\n\n"
        desc_stats = analyzer.get_descriptive_statistics()
        
        if desc_stats:
            markdown += "**Table 4.3:** Descriptive Statistics for Key Variables\n\n"
            markdown += "| Variable | N | Mean | SD | Min | Max |\n"
            markdown += "|----------|---|------|----|----|-----|\n"
            for var, stats in list(desc_stats.items())[:10]:
                markdown += f"| {var} | {total} | {stats['mean']:.2f} | {stats['std']:.2f} | {stats['min']} | {stats['max']} |\n"
            markdown += "\n"
        
        # Correlation analysis
        markdown += "## 4.4 Correlation Analysis\n\n"
        corr_results = analyzer.perform_correlation_analysis()
        
        if corr_results and corr_results['significant']:
            markdown += "**Table 4.4:** Significant Correlations Between Variables\n\n"
            markdown += "| Variable 1 | Variable 2 | Correlation (r) | Strength |\n"
            markdown += "|-----------|-----------|----------------|----------|\n"
            for corr in corr_results['significant'][:10]:
                markdown += f"| {corr['var1']} | {corr['var2']} | {corr['correlation']:.3f} | {corr['strength']} |\n"
            markdown += "\n"
            
            markdown += "The correlation analysis reveals several significant relationships between variables. "
            markdown += f"The strongest correlation was found between {corr_results['significant'][0]['var1']} and {corr_results['significant'][0]['var2']} "
            markdown += f"(r = {corr_results['significant'][0]['correlation']:.3f}), indicating a {corr_results['significant'][0]['strength']} relationship.\n\n"
        
        return markdown
    
    def _analyze_qualitative_data(self, csv_file, objectives):
        """Analyze qualitative data"""
        print("\n📝 Analyzing qualitative data...")
        
        analyzer = QualitativeAnalyzer(csv_file)
        markdown = ""
        
        markdown += "## 4.5 Qualitative Findings\n\n"
        markdown += "### 4.5.1 Participant Characteristics\n\n"
        
        demographics = analyzer.get_participant_demographics()
        
        if 'gender' in demographics:
            total = sum(demographics['gender'].values())
            markdown += f"A total of {total} participants were interviewed. "
            for gender, count in demographics['gender'].items():
                markdown += f"{count} were {gender.lower()}, "
            markdown += "providing diverse perspectives on the research topic.\n\n"
        
        # Thematic analysis
        markdown += "### 4.5.2 Thematic Analysis\n\n"
        themes = analyzer.extract_themes()
        thematic_summary = analyzer.generate_thematic_summary(themes)
        
        for theme_col, theme_info in thematic_summary.items():
            markdown += f"#### {theme_col}\n\n"
            markdown += f"**Table 4.X:** {theme_col} Frequency\n\n"
            markdown += "| Theme | Frequency | Percentage (%) |\n"
            markdown += "|-------|-----------|----------------|\n"
            for theme_data in theme_info['themes']:
                markdown += f"| {theme_data['theme'][:60]}... | {theme_data['frequency']} | {theme_data['percentage']:.1f} |\n"
            markdown += f"| **Total** | **{theme_info['total']}** | **100.0** |\n\n"
        
        # Representative quotes
        markdown += "### 4.5.3 Representative Quotes\n\n"
        quotes = analyzer.extract_quotes(limit=5)
        
        if quotes:
            for i, quote_data in enumerate(quotes, 1):
                markdown += f"**Quote {i}** ({quote_data['participant_id']}, {quote_data['gender']}, {quote_data['age']} years, {quote_data['occupation']}):\n"
                markdown += f"> \"{quote_data['quote']}\"\n\n"
        
        return markdown
    
    def save_analysis_report(self, content, output_dir="thesis/output"):
        """Save the analysis report"""
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{output_dir}/Chapter4_Analysis.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n✅ Analysis report saved: {filename}")
        return filename
