import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.textbook_planner import expand_section_to_topics, expand_topic_to_subsections, Topic

class MockGenerator:
    def generate(self, prompt, max_tokens=2000):
        # Return a mock list of items
        return "\n".join([f"{i}. Item {i}" for i in range(1, 16)])

def test_defaults():
    generator = MockGenerator()
    
    # Test topics default
    topics = expand_section_to_topics(generator, "Test Section")
    print(f"Topics count: {len(topics)}")
    assert len(topics) == 15, f"Expected 15 topics, got {len(topics)}"
    
    # Test subsections default
    topic = Topic("Test Topic")
    subsections = expand_topic_to_subsections(generator, "Test Section", topic)
    print(f"Subsections count: {len(subsections)}")
    assert len(subsections) == 4, f"Expected 4 subsections, got {len(subsections)}"
    
    print("✅ Defaults verification passed!")

if __name__ == "__main__":
    test_defaults()
