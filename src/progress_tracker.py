"""
Real-time Progress Tracker - Show live progress during generation
"""
import threading
import time
from datetime import datetime

class ProgressTracker:
    def __init__(self):
        self.lock = threading.Lock()
        self.sections = {}
        self.active = False
        self.display_thread = None
    
    def start_section(self, section_num: str, section_title: str, total_subsections: int):
        """Mark a section as started."""
        with self.lock:
            self.sections[section_num] = {
                'title': section_title,
                'status': 'generating',
                'total_subsections': total_subsections,
                'completed_subsections': 0,
                'current_subsection': None,
                'start_time': time.time(),
                'words': 0
            }
    
    def update_subsection(self, section_num: str, subsection_name: str):
        """Update current subsection being written."""
        with self.lock:
            if section_num in self.sections:
                self.sections[section_num]['current_subsection'] = subsection_name
    
    def complete_subsection(self, section_num: str, words: int = 0):
        """Mark a subsection as completed."""
        with self.lock:
            if section_num in self.sections:
                self.sections[section_num]['completed_subsections'] += 1
                self.sections[section_num]['words'] += words
    
    def complete_section(self, section_num: str, total_words: int):
        """Mark a section as completed."""
        with self.lock:
            if section_num in self.sections:
                self.sections[section_num]['status'] = 'complete'
                self.sections[section_num]['words'] = total_words
                self.sections[section_num]['end_time'] = time.time()
    
    def start_display(self):
        """Start the real-time display thread."""
        self.active = True
        self.display_thread = threading.Thread(target=self._display_loop, daemon=True)
        self.display_thread.start()
    
    def stop_display(self):
        """Stop the real-time display."""
        self.active = False
        if self.display_thread:
            self.display_thread.join(timeout=1)
    
    def _display_loop(self):
        """Display progress in real-time."""
        try:
            while self.active:
                self._print_progress()
                time.sleep(3)  # Update every 3 seconds
        except KeyboardInterrupt:
            pass  # Gracefully handle Ctrl+C
        except Exception:
            pass  # Ignore other errors during shutdown
    
    def _print_progress(self):
        """Print current progress."""
        with self.lock:
            if not self.sections:
                return
            
            # Clear screen and print header
            print("\033[2J\033[H")  # Clear screen and move cursor to top
            print("=" * 80)
            print("📊 REAL-TIME GENERATION PROGRESS")
            print("=" * 80)
            print(f"⏰ {datetime.now().strftime('%H:%M:%S')}\n")
            
            # Calculate totals
            total_sections = len(self.sections)
            completed_sections = sum(1 for s in self.sections.values() if s['status'] == 'complete')
            total_words = sum(s['words'] for s in self.sections.values())
            
            print(f"📚 Sections: {completed_sections}/{total_sections} complete")
            print(f"📝 Total words generated: {total_words:,}\n")
            print("-" * 80)
            
            # Show each section
            for section_num in sorted(self.sections.keys()):
                section = self.sections[section_num]
                
                # Status icon
                if section['status'] == 'complete':
                    icon = "✅"
                    status_text = "COMPLETE"
                else:
                    icon = "🔄"
                    status_text = "GENERATING"
                
                # Progress bar
                progress = section['completed_subsections'] / section['total_subsections']
                bar_length = 30
                filled = int(bar_length * progress)
                bar = "█" * filled + "░" * (bar_length - filled)
                
                # Time elapsed
                elapsed = time.time() - section['start_time']
                elapsed_str = f"{int(elapsed // 60)}m {int(elapsed % 60)}s"
                
                # Print section info
                print(f"\n{icon} Section {section_num}: {section['title'][:50]}")
                print(f"   Status: {status_text}")
                print(f"   Progress: [{bar}] {section['completed_subsections']}/{section['total_subsections']} subsections")
                print(f"   Words: {section['words']:,}")
                print(f"   Time: {elapsed_str}")
                
                if section['current_subsection'] and section['status'] != 'complete':
                    print(f"   Current: {section['current_subsection'][:60]}...")
            
            print("\n" + "=" * 80)
            print("💡 Tip: This updates every 3 seconds. Press Ctrl+C to stop.")
            print("=" * 80)

# Global instance
progress_tracker = ProgressTracker()
