from typing import List
from .generator import LLMGenerator
from .state_manager import Chapter, Scene

class Planner:
    def __init__(self, generator: LLMGenerator):
        self.generator = generator

    def generate_idea(self) -> str:
        prompt = "Generate a unique, high-concept idea for a 100,000 word novel. Focus on a strong hook and clear conflict."
        return self.generator.generate(prompt).strip()

    def create_global_outline(self, idea: str, num_chapters: int) -> List[Chapter]:
        prompt = f"""
        Create a detailed chapter-by-chapter outline for a novel based on this idea:
        "{idea}"
        
        There should be exactly {num_chapters} chapters.
        Format the output as a list of chapters with titles and brief summaries.
        """
        response = self.generator.generate(prompt)
        
        # Basic parsing: Split by "Chapter" and extract title/summary
        chapters = []
        lines = response.split('\n')
        current_title = ""
        current_summary = []
        
        for line in lines:
            if line.strip().lower().startswith("chapter"):
                if current_title:
                    chapters.append(Chapter(title=current_title, summary=" ".join(current_summary), scenes=[]))
                current_title = line.strip()
                current_summary = []
            else:
                if current_title:
                    current_summary.append(line.strip())
                    
        if current_title:
             chapters.append(Chapter(title=current_title, summary=" ".join(current_summary), scenes=[]))
             
        # Fallback if parsing failed
        if not chapters:
            print(f"Warning: Outline parsing failed. Response: {response[:100]}...")
            for i in range(1, num_chapters + 1):
                chapters.append(Chapter(
                    title=f"Chapter {i}",
                    summary=f"Summary for chapter {i} based on {idea[:20]}...",
                    scenes=[]
                ))
        
        return chapters[:num_chapters]

    def create_chapter_outline(self, chapter: Chapter, num_scenes: int) -> List[Scene]:
        prompt = f"""
        Break down the following chapter into {num_scenes} detailed scenes:
        Title: {chapter.title}
        Summary: {chapter.summary}
        
        For each scene, provide a title and a paragraph describing the action.
        """
        response = self.generator.generate(prompt)
        
        scenes = []
        for i in range(1, num_scenes + 1):
            scenes.append(Scene(
                title=f"Scene {i}",
                summary=f"Action for scene {i} of {chapter.title}..."
            ))
        return scenes
