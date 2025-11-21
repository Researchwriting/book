"""
Visualization Generator
Creates charts and graphs for data presentation
"""
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

class VisualizationGenerator:
    def __init__(self, output_dir="thesis/visualizations"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (10, 6)
    
    def create_bar_chart(self, data_dict, title, xlabel, ylabel, filename):
        """Create a bar chart"""
        print(f"  📊 Creating bar chart: {filename}")
        
        plt.figure(figsize=(10, 6))
        categories = list(data_dict.keys())
        values = list(data_dict.values())
        
        plt.bar(categories, values, color='steelblue')
        plt.title(title, fontsize=14, fontweight='bold')
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        filepath = f"{self.output_dir}/{filename}"
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def create_pie_chart(self, data_dict, title, filename):
        """Create a pie chart"""
        print(f"  🥧 Creating pie chart: {filename}")
        
        plt.figure(figsize=(8, 8))
        labels = list(data_dict.keys())
        sizes = list(data_dict.values())
        
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.axis('equal')
        
        filepath = f"{self.output_dir}/{filename}"
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def create_histogram(self, data_series, title, xlabel, filename, bins=20):
        """Create a histogram"""
        print(f"  📈 Creating histogram: {filename}")
        
        plt.figure(figsize=(10, 6))
        plt.hist(data_series, bins=bins, color='skyblue', edgecolor='black')
        plt.title(title, fontsize=14, fontweight='bold')
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.grid(axis='y', alpha=0.75)
        
        filepath = f"{self.output_dir}/{filename}"
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def create_correlation_heatmap(self, correlation_matrix, title, filename):
        """Create a correlation heatmap"""
        print(f"  🔥 Creating heatmap: {filename}")
        
        plt.figure(figsize=(12, 10))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                    square=True, linewidths=1, cbar_kws={"shrink": 0.8})
        plt.title(title, fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        filepath = f"{self.output_dir}/{filename}")
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def create_grouped_bar_chart(self, df, x_col, y_col, hue_col, title, filename):
        """Create a grouped bar chart"""
        print(f"  📊 Creating grouped bar chart: {filename}")
        
        plt.figure(figsize=(12, 6))
        sns.barplot(data=df, x=x_col, y=y_col, hue=hue_col)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.legend(title=hue_col)
        plt.tight_layout()
        
        filepath = f"{self.output_dir}/{filename}")
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath
