import json
import os
import hashlib

class ThesisStateManager:
    def __init__(self, topic="", state_file=None):
        # Create unique state file per topic
        if state_file is None and topic:
            topic_hash = hashlib.md5(topic.encode()).hexdigest()[:8]
            state_file = f"thesis/state_{topic_hash}.json"
        elif state_file is None:
            state_file = "thesis/state.json"
        
        self.state_file = state_file
        self.state = self._load_state()

    def _load_state(self):
        """Load state from JSON file."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading state: {e}")
                return {}
        return {}

    def save_section(self, chapter, section, content):
        """Save content for a specific section."""
        if chapter not in self.state:
            self.state[chapter] = {}
        
        self.state[chapter][section] = content
        self._save_state()

    def _save_state(self):
        """Save state to JSON file."""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self.state, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving state: {e}")


    def get_chapter_content(self, chapter):
        """Get all content for a specific chapter."""
        if chapter in self.state:
            return "\n\n".join(self.state[chapter].values())
        return ""
    
    def get_section_content(self, chapter, section):
        """Get content for a specific section."""
        if chapter in self.state and section in self.state[chapter]:
            return self.state[chapter][section]
        return ""

    def get_full_state(self):
        """Get the entire state."""
        return self.state
