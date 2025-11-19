import os
from dataclasses import dataclass
from enum import Enum

class LLMProvider(Enum):
    MOCK = "mock"
    GEMINI = "gemini"
    GEMINI_FLASH = "gemini-flash"  # Ultra-fast for production
    OPENAI = "openai"
    DEEPSEEK = "deepseek"

@dataclass
class Config:
    # General Settings
    PROJECT_NAME: str = "My 100k Novel"
    OUTPUT_DIR: str = "output"
    STATE_FILE: str = "state.json"
    
    # Generation Settings
    TARGET_TOTAL_WORDS: int = 100000
    CHAPTERS_COUNT: int = 30  # Approx 3300 words per chapter
    SCENES_PER_CHAPTER: int = 4 # Approx 800 words per scene
    
    # LLM Settings
    PROVIDER: LLMProvider = LLMProvider.DEEPSEEK
    API_KEY: str = "YOUR_API_KEY_HERE"
    MODEL_NAME: str = "deepseek-chat" 
    
    # Context Settings
    MAX_CONTEXT_WORDS: int = 4000 # DeepSeek has larger context
