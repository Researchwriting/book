from .generator import LLMGenerator
from .state_manager import Scene

class Writer:
    def __init__(self, generator: LLMGenerator):
        self.generator = generator

    def write_scene(self, scene: Scene, context: str) -> str:
        prompt = f"""
        Write the full prose for the following scene.
        
        Context (Previous events):
        {context}
        
        Current Scene:
        Title: {scene.title}
        Summary: {scene.summary}
        
        Write approximately 800-1000 words. Focus on sensory details and dialogue.
        """
        return self.generator.generate(prompt)
