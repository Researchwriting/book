"""
Output Organizer - Organize generated files by chapter/topic
"""
import os
import shutil
from pathlib import Path

class OutputOrganizer:
    def __init__(self, base_output_dir: str = "output"):
        self.base_output_dir = base_output_dir
    
    def create_chapter_structure(self, chapter_name: str) -> dict:
        """
        Create organized folder structure for a chapter.
        
        Args:
            chapter_name: Name of the chapter (will be sanitized)
        
        Returns:
            Dict with paths to different directories
        """
        # Sanitize chapter name
        safe_name = self._sanitize_name(chapter_name)
        
        # Create directory structure
        chapter_dir = os.path.join(self.base_output_dir, safe_name)
        sections_dir = os.path.join(chapter_dir, "sections")
        master_commands_dir = os.path.join(chapter_dir, "master_commands")
        
        os.makedirs(sections_dir, exist_ok=True)
        os.makedirs(master_commands_dir, exist_ok=True)
        
        return {
            'chapter_dir': chapter_dir,
            'sections_dir': sections_dir,
            'master_commands_dir': master_commands_dir
        }
    
    def get_section_path(self, chapter_name: str, section_file: str, file_type: str = 'md') -> str:
        """
        Get the organized path for a section file.
        
        Args:
            chapter_name: Name of the chapter
            section_file: Original section filename
            file_type: 'md' or 'docx'
        
        Returns:
            Full path to the organized file location
        """
        dirs = self.create_chapter_structure(chapter_name)
        
        # Ensure correct extension
        base_name = os.path.splitext(section_file)[0]
        filename = f"{base_name}.{file_type}"
        
        return os.path.join(dirs['sections_dir'], filename)
    
    def get_combined_path(self, chapter_name: str, file_type: str = 'md') -> str:
        """
        Get the path for the combined chapter file.
        
        Args:
            chapter_name: Name of the chapter
            file_type: 'md' or 'docx'
        
        Returns:
            Full path to the combined file location
        """
        dirs = self.create_chapter_structure(chapter_name)
        safe_name = self._sanitize_name(chapter_name)
        filename = f"Complete_{safe_name}.{file_type}"
        
        return os.path.join(dirs['chapter_dir'], filename)
    
    def get_master_command_path(self, chapter_name: str, section_num: str) -> str:
        """
        Get the path for a master command file.
        
        Args:
            chapter_name: Name of the chapter
            section_num: Section number
        
        Returns:
            Full path to the master command file
        """
        dirs = self.create_chapter_structure(chapter_name)
        filename = f"Section_{section_num}_Master_Command.md"
        
        return os.path.join(dirs['master_commands_dir'], filename)
    
    def _sanitize_name(self, name: str) -> str:
        """Sanitize name for use as directory name."""
        # Remove special characters, keep alphanumeric, spaces, hyphens, underscores
        safe = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_'))
        # Replace spaces with underscores
        safe = safe.replace(' ', '_')
        # Remove multiple underscores
        while '__' in safe:
            safe = safe.replace('__', '_')
        return safe.strip('_')
    
    def organize_existing_files(self):
        """
        Organize existing files in output/ into chapter structure.
        Useful for migrating old files.
        """
        if not os.path.exists(self.base_output_dir):
            return
        
        # Find all section files
        section_files = []
        for file in os.listdir(self.base_output_dir):
            if file.startswith('Section_') and (file.endswith('.md') or file.endswith('.docx')):
                section_files.append(file)
        
        if not section_files:
            return
        
        print(f"\n📁 Organizing {len(section_files)} existing files...")
        
        # Group by chapter (assume all belong to same chapter for now)
        # In real use, this would parse the chapter name from files
        default_chapter = "Textbook_Sections"
        
        for file in section_files:
            old_path = os.path.join(self.base_output_dir, file)
            
            if file.endswith('.md'):
                new_path = self.get_section_path(default_chapter, file, 'md')
            else:
                new_path = self.get_section_path(default_chapter, file, 'docx')
            
            # Move file
            os.makedirs(os.path.dirname(new_path), exist_ok=True)
            shutil.move(old_path, new_path)
            print(f"  ✅ Moved: {file} → {os.path.relpath(new_path)}")
        
        print(f"✅ Organization complete!")

# Global instance
output_organizer = OutputOrganizer()
