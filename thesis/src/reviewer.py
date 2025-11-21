from .llm import LLMClient
import os

class ReviewerPanel:
    def __init__(self, llm_client):
        self.llm = llm_client
        self.reviewers = [
            {
                "name": "Reviewer 1 (Supportive Mentor)",
                "role": "supportive",
                "prompt": """You are a supportive academic mentor reviewing a PhD thesis section.
                
TASK: Review the following section and provide constructive feedback.

FOCUS ON:
- Structure and organization
- Clarity of arguments
- Academic tone and language
- Strengths and areas for improvement

TONE: Encouraging but thorough. Identify both strengths and weaknesses.

RECOMMENDATION: Provide a decision (Accept, Minor Revisions, Major Revisions, Reject)"""
            },
            {
                "name": "Reviewer 2 (Harsh Critic)",
                "role": "harsh",
                "prompt": """You are an extremely critical peer reviewer known for rejecting most papers.
                
TASK: Find EVERY possible flaw in the following section. Be ruthless.

FOCUS ON:
- Weak arguments and logical fallacies
- Missing or insufficient citations
- Methodological gaps
- Overgeneralizations
- Lack of rigor
- Poor evidence

TONE: Extremely critical. Demand perfection. Find problems others miss.

RECOMMENDATION: Almost always recommend Reject or Major Revisions. Be specific about what's wrong."""
            },
            {
                "name": "Reviewer 3 (Methodologist)",
                "role": "methodologist",
                "prompt": """You are a methodologist focused on research rigor and evidence quality.
                
TASK: Evaluate the research quality and methodological soundness.

FOCUS ON:
- Research design validity
- Data quality and sources
- Appropriateness of methods
- Validity of conclusions
- Evidence-based claims
- Theoretical framework

TONE: Analytical and precise. Focus on scientific rigor.

RECOMMENDATION: Provide a decision based on methodological soundness."""
            }
        ]

    def review_section(self, content, section_title, chapter_title):
        """
        Generate reviews from all 3 reviewers.
        """
        print(f"  📋 Peer review in progress...")
        
        reviews = []
        for reviewer in self.reviewers:
            print(f"    - {reviewer['name']}...")
            
            full_prompt = f"""{reviewer['prompt']}

CHAPTER: {chapter_title}
SECTION: {section_title}

CONTENT TO REVIEW:
{content}

Provide your review in the following format:
1. Summary of the section
2. Strengths (if any)
3. Weaknesses/Issues
4. Specific recommendations for improvement
5. Overall recommendation (Accept/Minor Revisions/Major Revisions/Reject)
"""
            
            review_text = self.llm.generate(
                full_prompt,
                system_prompt=f"You are {reviewer['name']}, a peer reviewer for an academic journal.",
                max_tokens=2048
            )
            
            reviews.append({
                "reviewer": reviewer['name'],
                "role": reviewer['role'],
                "review": review_text
            })
        
        return reviews

    def improve_based_on_reviews(self, content, reviews, section_title):
        """
        Rewrite content addressing all reviewer feedback.
        """
        print(f"  ✍️  Revising based on peer feedback...")
        
        # Compile all feedback
        feedback_summary = "\n\n".join([
            f"### {r['reviewer']}\n{r['review']}" for r in reviews
        ])
        
        improvement_prompt = f"""You are revising a PhD thesis section based on peer review feedback.

ORIGINAL SECTION: {section_title}

ORIGINAL CONTENT:
{content}

PEER REVIEW FEEDBACK:
{feedback_summary}

TASK:
Rewrite the section to address ALL the feedback from all reviewers. Specifically:
1. Fix all issues raised by Reviewer 2 (the harsh critic)
2. Incorporate suggestions from Reviewer 1
3. Address methodological concerns from Reviewer 3
4. Maintain the original length (~1500-2000 words)
5. Keep Harvard referencing style
6. Ensure academic tone

Return ONLY the improved content, no commentary.
"""
        
        improved_content = self.llm.generate(
            improvement_prompt,
            system_prompt="You are a PhD candidate revising your thesis based on peer review.",
            max_tokens=4096
        )
        
        return improved_content

    def save_review_report(self, reviews, section_title, chapter_title, output_dir="thesis/reviews"):
        """
        Save review report to file.
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Create safe filename
        safe_chapter = chapter_title.replace(" ", "_").replace("/", "-")
        safe_section = section_title.replace(" ", "_").replace("/", "-")
        filename = f"{output_dir}/Review_{safe_chapter}_{safe_section}.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# Peer Review Report\n\n")
            f.write(f"**Chapter:** {chapter_title}\n")
            f.write(f"**Section:** {section_title}\n\n")
            f.write("---\n\n")
            
            for review in reviews:
                f.write(f"## {review['reviewer']}\n\n")
                f.write(review['review'])
                f.write("\n\n---\n\n")
            
            f.write("## Final Decision\n\n")
            f.write("All feedback has been addressed in the revised version.\n")
        
        return filename
