"""
Qualitative Data Analyzer
Performs thematic analysis on qualitative datasets (interviews, FGDs)
"""
import pandas as pd
import re

class QualitativeAnalyzer:
    def __init__(self, csv_file):
        """Initialize with path to CSV dataset"""
        self.csv_file = csv_file
        self.df = pd.read_csv(csv_file)
        print(f"📝 Loaded qualitative dataset: {len(self.df)} participants")
    
    def extract_themes(self):
        """Extract and categorize themes from responses"""
        print("  🎯 Extracting themes...")
        
        themes = {}
        
        # Get theme columns
        theme_cols = [col for col in self.df.columns if 'Theme' in col or 'Response' in col]
        
        for col in theme_cols:
            if col in self.df.columns:
                # Count theme occurrences
                theme_counts = self.df[col].value_counts()
                themes[col] = theme_counts.to_dict()
        
        return themes
    
    def extract_quotes(self, theme=None, limit=10):
        """Extract representative quotes"""
        print(f"  💬 Extracting quotes...")
        
        quotes = []
        
        if 'Key_Quotes' in self.df.columns:
            quote_col = 'Key_Quotes'
        else:
            # Find any column with quotes
            quote_col = [col for col in self.df.columns if 'quote' in col.lower()]
            quote_col = quote_col[0] if quote_col else None
        
        if quote_col:
            unique_quotes = self.df[quote_col].dropna().unique()
            for quote in unique_quotes[:limit]:
                # Find participant info
                participant = self.df[self.df[quote_col] == quote].iloc[0]
                quotes.append({
                    'quote': quote,
                    'participant_id': participant.get('ParticipantID', 'Unknown'),
                    'gender': participant.get('Gender', 'Unknown'),
                    'age': participant.get('Age', 'Unknown'),
                    'occupation': participant.get('Occupation', 'Unknown')
                })
        
        return quotes
    
    def get_participant_demographics(self):
        """Get demographic summary of participants"""
        print("  👥 Analyzing participant demographics...")
        
        demographics = {}
        
        # Gender distribution
        if 'Gender' in self.df.columns:
            demographics['gender'] = self.df['Gender'].value_counts().to_dict()
        
        # Age statistics
        if 'Age' in self.df.columns:
            demographics['age'] = {
                'mean': self.df['Age'].mean(),
                'min': self.df['Age'].min(),
                'max': self.df['Age'].max(),
                'range': f"{int(self.df['Age'].min())}-{int(self.df['Age'].max())}"
            }
        
        # Occupation distribution
        if 'Occupation' in self.df.columns:
            demographics['occupation'] = self.df['Occupation'].value_counts().to_dict()
        
        # Location distribution
        if 'Location' in self.df.columns:
            demographics['location'] = self.df['Location'].value_counts().to_dict()
        
        return demographics
    
    def generate_thematic_summary(self, themes):
        """Generate summary of themes with frequencies"""
        print("  📊 Generating thematic summary...")
        
        summary = {}
        
        for theme_col, theme_data in themes.items():
            total_responses = sum(theme_data.values())
            summary[theme_col] = {
                'total': total_responses,
                'themes': []
            }
            
            for theme, count in theme_data.items():
                percentage = (count / total_responses * 100)
                summary[theme_col]['themes'].append({
                    'theme': theme,
                    'frequency': count,
                    'percentage': percentage
                })
        
        return summary
    
    def perform_content_analysis(self, text_column):
        """Perform Content Analysis (word frequency, key terms)"""
        print("  📄 Performing content analysis...")
        
        from collections import Counter
        import re
        
        # Combine all text
        all_text = ' '.join(self.df[text_column].dropna().astype(str))
        
        # Clean and tokenize
        words = re.findall(r'\b\w+\b', all_text.lower())
        
        # Remove stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been', 'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'}
        filtered_words = [w for w in words if w not in stop_words and len(w) > 3]
        
        # Count frequencies
        word_freq = Counter(filtered_words)
        
        return {
            'total_words': len(words),
            'unique_words': len(set(words)),
            'top_20_words': word_freq.most_common(20),
            'lexical_diversity': len(set(words)) / len(words) if words else 0
        }
    
    def perform_document_analysis(self, document_column):
        """Perform Document Analysis (coding, categorization)"""
        print("  📋 Performing document analysis...")
        
        # Code documents by themes
        coded_documents = {}
        
        for idx, doc in self.df[document_column].dropna().items():
            # Simple keyword-based coding (can be enhanced with NLP)
            codes = []
            
            doc_lower = str(doc).lower()
            
            # Define coding categories
            if any(word in doc_lower for word in ['employ', 'job', 'work']):
                codes.append('Employment')
            if any(word in doc_lower for word in ['war', 'conflict', 'violence']):
                codes.append('Conflict')
            if any(word in doc_lower for word in ['economic', 'income', 'money']):
                codes.append('Economic')
            if any(word in doc_lower for word in ['government', 'policy', 'support']):
                codes.append('Government')
            if any(word in doc_lower for word in ['family', 'children', 'household']):
                codes.append('Family')
            
            coded_documents[idx] = codes
        
        # Count code frequencies
        code_freq = Counter([code for codes in coded_documents.values() for code in codes])
        
        return {
            'coded_documents': coded_documents,
            'code_frequencies': dict(code_freq),
            'total_codes': sum(code_freq.values())
        }
    
    def perform_narrative_analysis(self, narrative_column):
        """Perform Narrative Analysis (story structure, plot elements)"""
        print("  📖 Performing narrative analysis...")
        
        narratives = self.df[narrative_column].dropna()
        
        # Analyze narrative elements
        narrative_elements = {
            'total_narratives': len(narratives),
            'avg_length': narratives.str.len().mean(),
            'temporal_markers': 0,
            'causal_markers': 0,
            'emotional_markers': 0
        }
        
        # Count markers
        for narrative in narratives:
            narrative_lower = str(narrative).lower()
            
            # Temporal markers
            if any(word in narrative_lower for word in ['before', 'after', 'then', 'when', 'during']):
                narrative_elements['temporal_markers'] += 1
            
            # Causal markers
            if any(word in narrative_lower for word in ['because', 'therefore', 'thus', 'so', 'caused']):
                narrative_elements['causal_markers'] += 1
            
            # Emotional markers
            if any(word in narrative_lower for word in ['felt', 'sad', 'happy', 'angry', 'fear', 'hope']):
                narrative_elements['emotional_markers'] += 1
        
        return narrative_elements
    
    def perform_discourse_analysis(self, text_column):
        """Perform Discourse Analysis (power relations, ideologies)"""
        print("  💬 Performing discourse analysis...")
        
        texts = self.df[text_column].dropna()
        
        # Analyze discourse patterns
        discourse_patterns = {
            'passive_voice_count': 0,
            'modal_verbs_count': 0,
            'negative_constructions': 0,
            'collective_pronouns': 0
        }
        
        for text in texts:
            text_lower = str(text).lower()
            
            # Passive voice indicators
            if any(phrase in text_lower for phrase in ['was ', 'were ', 'been ', 'being ']):
                discourse_patterns['passive_voice_count'] += 1
            
            # Modal verbs (uncertainty, obligation)
            if any(word in text_lower for word in ['should', 'must', 'might', 'could', 'would']):
                discourse_patterns['modal_verbs_count'] += 1
            
            # Negative constructions
            if any(word in text_lower for word in ['not', 'no', 'never', 'nothing', 'cannot']):
                discourse_patterns['negative_constructions'] += 1
            
            # Collective pronouns
            if any(word in text_lower for word in ['we', 'us', 'our', 'they', 'them']):
                discourse_patterns['collective_pronouns'] += 1
        
        return discourse_patterns
    
    def generate_markdown_report(self, demographics, themes, quotes):
        """Generate markdown formatted qualitative analysis report"""
        print("  📝 Generating markdown report...")
        
        markdown = "# Qualitative Data Analysis\n\n"
        
        # Participant demographics
        markdown += "## Participant Demographics\n\n"
        
        if 'gender' in demographics:
            markdown += "### Gender Distribution\n\n"
            markdown += "| Gender | Frequency |\n"
            markdown += "|--------|----------|\n"
            for gender, count in demographics['gender'].items():
                markdown += f"| {gender} | {count} |\n"
            markdown += "\n"
        
        if 'occupation' in demographics:
            markdown += "### Occupation Distribution\n\n"
            markdown += "| Occupation | Frequency |\n"
            markdown += "|-----------|----------|\n"
            for occ, count in demographics['occupation'].items():
                markdown += f"| {occ} | {count} |\n"
            markdown += "\n"
        
        # Themes
        markdown += "## Thematic Analysis\n\n"
        
        for theme_col, theme_data in themes.items():
            markdown += f"### {theme_col}\n\n"
            markdown += "| Theme | Frequency | Percentage (%) |\n"
            markdown += "|-------|-----------|----------------|\n"
            total = sum(theme_data.values())
            for theme, count in theme_data.items():
                pct = (count / total * 100)
                markdown += f"| {theme[:50]}... | {count} | {pct:.1f} |\n"
            markdown += "\n"
        
        # Quotes
        if quotes:
            markdown += "## Representative Quotes\n\n"
            for i, quote_data in enumerate(quotes[:5], 1):
                markdown += f"**Quote {i}** ({quote_data['participant_id']}, {quote_data['gender']}, {quote_data['occupation']}):\n"
                markdown += f"> \"{quote_data['quote']}\"\n\n"
        
        return markdown
