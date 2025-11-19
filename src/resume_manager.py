"""
Resume Manager - Save and resume generation progress
"""
import json
import os
from typing import Dict, Optional

class ResumeManager:
    def __init__(self, state_file: str = "output/.generation_state.json"):
        self.state_file = state_file
        self.state = self.load_state()
    
    def load_state(self) -> Dict:
        """Load saved state from file."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_state(self):
        """Save current state to file."""
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def start_section(self, section_num: str, section_title: str, total_topics: int):
        """Mark section as started."""
        self.state[section_num] = {
            'section_title': section_title,
            'status': 'in_progress',
            'total_topics': total_topics,
            'completed_topics': [],
            'current_topic': None
        }
        self.save_state()
    
    def complete_subsection(self, section_num: str, topic_idx: int, subsection_idx: int):
        """Mark a subsection as completed."""
        if section_num in self.state:
            key = f"{topic_idx}.{subsection_idx}"
            if 'completed_subsections' not in self.state[section_num]:
                self.state[section_num]['completed_subsections'] = []
            
            if key not in self.state[section_num]['completed_subsections']:
                self.state[section_num]['completed_subsections'].append(key)
            
            self.save_state()
    
    def complete_topic(self, section_num: str, topic_idx: int):
        """Mark a topic as completed."""
        if section_num in self.state:
            if topic_idx not in self.state[section_num]['completed_topics']:
                self.state[section_num]['completed_topics'].append(topic_idx)
            self.save_state()
    
    def complete_section(self, section_num: str):
        """Mark section as completed."""
        if section_num in self.state:
            self.state[section_num]['status'] = 'completed'
            self.save_state()
    
    def is_section_started(self, section_num: str) -> bool:
        """Check if section has been started."""
        return section_num in self.state
    
    def is_section_completed(self, section_num: str) -> bool:
        """Check if section is completed."""
        return (section_num in self.state and 
                self.state[section_num].get('status') == 'completed')
    
    def is_subsection_completed(self, section_num: str, topic_idx: int, subsection_idx: int) -> bool:
        """Check if a specific subsection is completed."""
        if section_num not in self.state:
            return False
        
        key = f"{topic_idx}.{subsection_idx}"
        completed = self.state[section_num].get('completed_subsections', [])
        return key in completed
    
    def get_resume_point(self, section_num: str) -> Optional[Dict]:
        """Get the point to resume from for a section."""
        if section_num not in self.state:
            return None
        
        if self.state[section_num].get('status') == 'completed':
            return None
        
        return {
            'section_num': section_num,
            'completed_subsections': self.state[section_num].get('completed_subsections', []),
            'completed_topics': self.state[section_num].get('completed_topics', [])
        }
    
    def clear_section(self, section_num: str):
        """Clear state for a section (for restart)."""
        if section_num in self.state:
            del self.state[section_num]
            self.save_state()
    
    def get_summary(self) -> Dict:
        """Get summary of all sections."""
        summary = {
            'total_sections': len(self.state),
            'completed_sections': 0,
            'in_progress_sections': 0,
            'sections': {}
        }
        
        for section_num, data in self.state.items():
            status = data.get('status', 'unknown')
            if status == 'completed':
                summary['completed_sections'] += 1
            elif status == 'in_progress':
                summary['in_progress_sections'] += 1
            
            summary['sections'][section_num] = {
                'title': data.get('section_title', 'Unknown'),
                'status': status,
                'progress': f"{len(data.get('completed_subsections', []))} subsections"
            }
        
        return summary

# Global instance
resume_manager = ResumeManager()
