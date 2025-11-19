"""
Textbook Planner - Hierarchical expansion for textbook sections
"""
from typing import List
from src.generator import LLMGenerator

class Topic:
    def __init__(self, title: str, subsections: List[str] = None):
        self.title = title
        self.subsections = subsections or []

def expand_section_to_topics(generator: LLMGenerator, section_title: str, num_topics: int = 15) -> List[Topic]:
    """
    Expand a section into multiple topics.
    
    Args:
        generator: LLM generator
        section_title: The section title (e.g., "Digital and Online Research Methods")
        num_topics: Number of topics to generate
    
    Returns:
        List of Topic objects
    """
    prompt = f"""You are creating a detailed university textbook chapter section.

Section Title: {section_title}

Your task: Break this section into {num_topics} major topics that will be covered in depth.

REQUIREMENTS:
- Each topic should be a distinct, important aspect of {section_title}
- Topics should be comprehensive and cover the full scope
- Use clear, academic language
- Format: Return ONLY a numbered list, one topic per line
- Example format:
1. Topic Title One
2. Topic Title Two
...

Generate {num_topics} topics now:"""

    response = generator.generate(prompt, max_tokens=2000)
    
    # Parse the response
    topics = []
    lines = response.split('\n')
    for line in lines:
        line = line.strip()
        if line and (line[0].isdigit() or line.startswith('-')):
            # Remove numbering
            topic_text = line.split('.', 1)[-1].strip()
            if topic_text:
                topics.append(Topic(title=topic_text))
    
    # Fallback if parsing failed
    if not topics:
        print(f"Warning: Topic parsing failed. Using generic topics.")
        for i in range(1, num_topics + 1):
            topics.append(Topic(title=f"Topic {i}: Aspect of {section_title}"))
    
    return topics[:num_topics]

def expand_topic_to_subsections(generator: LLMGenerator, section_title: str, topic: Topic, num_subsections: int = 4) -> List[str]:
    """
    Expand a topic into subsections.
    
    Args:
        generator: LLM generator
        section_title: The parent section title
        topic: The Topic object
        num_subsections: Number of subsections
    
    Returns:
        List of subsection titles
    """
    prompt = f"""You are creating a detailed university textbook.

Section: {section_title}
Topic: {topic.title}

Your task: Break this topic into {num_subsections} subsections for detailed coverage.

REQUIREMENTS:
- Each subsection should cover a specific aspect of the topic
- Subsections should be logical and flow well
- Use clear, academic language
- Format: Return ONLY a numbered list
- Example:
1. Subsection Title One
2. Subsection Title Two
...

Generate {num_subsections} subsections now:"""

    response = generator.generate(prompt, max_tokens=1500)
    
    # Parse
    subsections = []
    lines = response.split('\n')
    for line in lines:
        line = line.strip()
        if line and (line[0].isdigit() or line.startswith('-')):
            subsection_text = line.split('.', 1)[-1].strip()
            if subsection_text:
                subsections.append(subsection_text)
    
    # Fallback
    if not subsections:
        for i in range(1, num_subsections + 1):
            subsections.append(f"Subsection {i}")
    
    return subsections[:num_subsections]
