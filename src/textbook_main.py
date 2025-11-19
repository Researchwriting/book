"""
Main Orchestrator for Textbook Generation
"""
import os
from src.config import Config
from src.generator import get_generator
from src.syllabus_parser import parse_syllabus
from src.textbook_planner import expand_section_to_topics, expand_topic_to_subsections
from src.textbook_writer import write_section_introduction, write_subsection, write_section_summary

def generate_textbook():
    """Main function to generate the textbook."""
    config = Config()
    generator = get_generator(config)
    
    print("=" * 60)
    print("TEXTBOOK GENERATOR - DeepSeek Edition")
    print("=" * 60)
    
    # Parse syllabus
    syllabus_path = "syllabus.md"
    sections = parse_syllabus(syllabus_path)
    
    print(f"\nFound {len(sections)} sections to generate.")
    print(f"Target: ~40,000 words per section")
    print(f"Total estimated output: ~{len(sections) * 40000} words\n")
    
    # Create output directory
    os.makedirs("output", exist_ok=True)
    
    # Process each section
    for idx, section_info in enumerate(sections, 1):
        chapter = section_info['chapter']
        section_num = section_info['section_number']
        section_title = section_info['section_title']
        
        print(f"\n{'='*60}")
        print(f"Processing Section {section_num}: {section_title}")
        print(f"{'='*60}\n")
        
        # Step 1: Expand to topics
        print(f"  [1/4] Planning content structure...")
        topics = expand_section_to_topics(generator, section_title)
        
        # Step 2: Expand topics to subsections
        for topic in topics:
            subsections = expand_topic_to_subsections(generator, section_title, topic)
            topic.subsections = subsections
        print(f"  Structure ready ({len(topics)} topics, {sum(len(t.subsections) for t in topics)} subsections)")
        
        # Step 3: Write content
        print(f"  [3/4] Writing content...")
        
        # Open file for writing
        filename = f"output/Section_{section_num}_{section_title.replace(' ', '_')}.md"
        word_count = 0
        
        with open(filename, 'w', encoding='utf-8') as f:
            # Write header
            f.write(f"# {chapter}\n\n")
            f.write(f"## Section {section_num}: {section_title}\n\n")
            
            # Introduction
            intro = write_section_introduction(generator, section_title, topics)
            f.write(intro + "\n\n")
            word_count += len(intro.split())
            f.flush()  # Force write to disk
            
            # Write each topic and its subsections
            for topic_idx, topic in enumerate(topics, 1):
                f.write(f"### {section_num}.{topic_idx} {topic.title}\n\n")
                
                for subsection_idx, subsection in enumerate(topic.subsections, 1):
                    print(f"    Writing: {topic.title} > {subsection}...")
                    subsection_content = write_subsection(
                        generator,
                        section_title,
                        topic.title,
                        subsection,
                        target_words=1000
                    )
                    f.write(f"#### {section_num}.{topic_idx}.{subsection_idx} {subsection}\n\n")
                    f.write(subsection_content + "\n\n")
                    word_count += len(subsection_content.split())
                    f.flush()  # Write to disk after each subsection
            
            # Summary
            summary = write_section_summary(generator, section_title, topics)
            f.write(f"### Summary and Reflection\n\n")
            f.write(summary + "\n\n")
            word_count += len(summary.split())
            f.flush()
        
        print(f"  [4/4] Saved to {filename}")
        print(f"  Total words: ~{word_count}")
        print(f"  Section {section_num} complete!\n")
    
    # Combine all sections into one document
    print(f"\n{'='*60}")
    print("Combining all sections into final document...")
    print(f"{'='*60}\n")
    
    combined_content = ""
    for idx, section_info in enumerate(sections, 1):
        section_num = section_info['section_number']
        section_title = section_info['section_title']
        filename = f"output/Section_{section_num}_{section_title.replace(' ', '_')}.md"
        
        with open(filename, 'r', encoding='utf-8') as f:
            combined_content += f.read() + "\n\n"
    
    # Save combined document
    combined_filename = "output/Complete_Textbook.md"
    with open(combined_filename, 'w', encoding='utf-8') as f:
        f.write(combined_content)
    
    print(f"✅ Complete textbook saved to: {combined_filename}")
    print(f"✅ Total sections: {len(sections)}")
    print(f"✅ Estimated total words: ~{len(sections) * 40000}")
    print("\nGeneration complete!")

if __name__ == "__main__":
    generate_textbook()
