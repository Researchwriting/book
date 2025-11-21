#!/usr/bin/env python3
"""
Quick Test Script for Thesis Generator
Tests the full pipeline (planning, research, drafting, peer review, references) 
on only sections 1.1 and 1.4 of Chapter 1.
"""

import os
import sys

# Add thesis to path as a package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'thesis'))

from src.structure import ThesisStructure
from src.writer import ThesisWriter
from src.config import Config
from src.state_manager import ThesisStateManager
from src.planner import ChapterPlanner
from src.reference_manager import ReferenceManager

def main():
    print("=" * 70)
    print("🧪 THESIS GENERATOR - QUICK TEST")
    print("=" * 70)
    print("\nTesting with Chapter 1, Sections 1.1 and 1.4 only\n")
    
    # Test parameters
    topic = "Impact of Wars in Africa"
    case_study = "South Sudan"
    
    print(f"Topic: {topic}")
    print(f"Case Study: {case_study}")
    print("=" * 70)
    
    # Initialize components (same as main script)
    state_manager = ThesisStateManager(topic=topic)
    reference_manager = ReferenceManager(topic=topic)
    planner = ChapterPlanner()
    writer = ThesisWriter(state_manager, reference_manager)
    structure = ThesisStructure.get_structure()
    
    # Get Chapter 1 structure
    chapter_key = "CHAPTER ONE"
    chapter_data = structure[chapter_key]
    
    # Test sections
    test_sections = [
        "1.1 Setting the scene",
        "1.4 Objectives"
    ]
    
    # Create output directory
    os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
    filename = f"{Config.OUTPUT_DIR}/TEST_Thesis_{topic.replace(' ', '_')[:30]}.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        # Write header
        f.write(f"# TEST THESIS: {topic}\n\n")
        f.write(f"**Case Study:** {case_study}\n\n")
        f.write("**Note:** This is a test generation of sections 1.1 and 1.4 only.\n\n")
        f.write("---\n\n")
        
        print(f"\n📚 Processing {chapter_key}: {chapter_data['title']}")
        
        # Generate custom outline
        custom_outline = planner.plan_chapter(chapter_key, chapter_data['title'], topic, case_study)
        
        f.write(f"# {chapter_key}\n")
        f.write(f"## {chapter_data['title']}\n\n")
        
        for section in test_sections:
            if section not in chapter_data['sections']:
                print(f"⚠️  Warning: {section} not in structure, skipping...")
                continue
                
            print(f"\n   Writing section: {section}...")
            
            # Check for custom subsections
            subsections = custom_outline.get(section, [])
            
            if subsections:
                print(f"   Using custom outline: {subsections}")
                f.write(f"### {section}\n\n")
                
                for subsection in subsections:
                    print(f"     - {subsection}...")
                    content = writer.write_section(chapter_data['title'], f"{section} - {subsection}", topic, case_study)
                    f.write(f"#### {subsection}\n\n")
                    f.write(content + "\n\n")
                    f.flush()
                
                combined_content = f"[Custom outline with subsections: {', '.join(subsections)}]"
                state_manager.save_section(chapter_key, section, combined_content)
            else:
                # Standard section writing
                content = writer.write_section(chapter_data['title'], section, topic, case_study)
                state_manager.save_section(chapter_key, section, content)
                
                f.write(f"### {section}\n\n")
                f.write(content + "\n\n")
                f.flush()
            
            print(f"   ✅ {section} Complete!")
    
    print(f"\n🎉 Test generation complete!")
    print(f"📄 Thesis saved to: {filename}")
    
    # Generate bibliography
    print("\n📚 Generating bibliography...")
    bib_file = reference_manager.generate_bibliography()
    print(f"📚 Bibliography saved to: {bib_file}")
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    print(f"✅ Sections generated: {len(test_sections)}")
    print(f"✅ Thesis output: {filename}")
    print(f"✅ Bibliography: {bib_file}")
    print(f"✅ References DB: {reference_manager.ref_file}")
    print(f"✅ State file: {state_manager.state_file}")
    print(f"✅ Review reports: thesis/reviews/")
    print("=" * 70)

if __name__ == "__main__":
    main()
