import json
import os
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

@dataclass
class Scene:
    title: str
    summary: str
    content: str = ""
    status: str = "pending" # pending, generating, completed

@dataclass
class Chapter:
    title: str
    summary: str
    scenes: List[Scene]
    status: str = "pending"

@dataclass
class ProjectState:
    idea: str = ""
    outline: List[Chapter] = None
    current_chapter_index: int = 0
    current_scene_index: int = 0
    total_words: int = 0
    
    def __post_init__(self):
        if self.outline is None:
            self.outline = []

class StateManager:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.state = ProjectState()

    def save(self):
        data = asdict(self.state)
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def load(self):
        if not os.path.exists(self.filepath):
            return
        
        with open(self.filepath, 'r') as f:
            data = json.load(f)
            
        # Reconstruct objects
        self.state.idea = data.get("idea", "")
        self.state.current_chapter_index = data.get("current_chapter_index", 0)
        self.state.current_scene_index = data.get("current_scene_index", 0)
        self.state.total_words = data.get("total_words", 0)
        
        raw_outline = data.get("outline", [])
        self.state.outline = []
        for ch_data in raw_outline:
            scenes = []
            for sc_data in ch_data.get("scenes", []):
                scenes.append(Scene(**sc_data))
            
            ch_data['scenes'] = scenes
            self.state.outline.append(Chapter(**ch_data))

    def update_scene_content(self, chapter_idx: int, scene_idx: int, content: str):
        if 0 <= chapter_idx < len(self.state.outline):
            chapter = self.state.outline[chapter_idx]
            if 0 <= scene_idx < len(chapter.scenes):
                scene = chapter.scenes[scene_idx]
                scene.content = content
                scene.status = "completed"
                # Simple word count estimation
                self.state.total_words += len(content.split())
                self.save()
