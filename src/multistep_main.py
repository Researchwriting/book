"""
Multi-Step Textbook Generator with Real-Time Progress
"""
import os
import time
from src.config import Config
from src.generator import get_generator
from src.syllabus_parser import parse_syllabus
from src.master_command_generator import generate_master_command
from src.textbook_planner import expand_section_to_topics, expand_topic_to_subsections
from src.textbook_writer import write_section_introduction, write_subsection, write_section_summary

def generate_textbook_multistep():
    """
    Multi-step generation with real-time progress visibility.
    
    Steps:
    1. Parse syllabus
    2. Generate Master Commands for each section
    3. Process each section independently
    4. Show real-time file updates
    """
    config = Config()
    generator = get_generator(config)
    
    print("=" * 70)
    print("MULTI-STEP TEXTBOOK GENERATOR - DeepSeek Edition")
    print("=" * 70)
    
    # Parse syllabus
    syllabus_path = "syllabus.md"
    sections = parse_syllabus(syllabus_path)
    
    print(f"\n📚 Found {len(sections)} sections to generate.")
    print(f"🎯 Target: ~40,000 words per section")
    print(f"📊 Total estimated output: ~{len(sections) * 40000:,} words\n")
    
    # Create output directory
    os.makedirs("output", exist_ok=True)
    os.makedirs("output/master_commands", exist_ok=True)
    
    # STEP 1: Generate Master Commands
    print("\n" + "=" * 70)
    print("STEP 1: Generating Master Commands for Each Section")
    print("=" * 70 + "\n")
    
    for idx, section_info in enumerate(sections, 1):
        section_num = section_info['section_number']
        section_title = section_info['section_title']
        
        print(f"  [{idx}/{len(sections)}] Creating Master Command for Section {section_num}: {section_title}")
        
        master_command = generate_master_command(section_info)
        
        # Save Master Command
        mc_filename = f"output/master_commands/Section_{section_num}_Master_Command.md"
        with open(mc_filename, 'w', encoding='utf-8') as f:
            f.write(master_command)
        
        print(f"      ✅ Saved to {mc_filename}")
    
    print(f"\n✅ All Master Commands generated!")
    print(f"📁 Location: output/master_commands/\n")
    
    # STEP 2: Process Each Section
    print("\n" + "=" * 70)
    print("STEP 2: Generating Content for Each Section")
    print("=" * 70 + "\n")
    
    for idx, section_info in enumerate(sections, 1):
        chapter = section_info['chapter']
        section_num = section_info['section_number']
        section_title = section_info['section_title']
        
        print(f"\n{'='*70}")
        print(f"📝 Processing Section {section_num}/{len(sections)}: {section_title}")
        print(f"{'='*70}\n")
        
        # Create output file immediately
        filename = f"output/Section_{section_num}_{section_title.replace(' ', '_')}.md"
        
        # Open file for real-time writing
        with open(filename, 'w', encoding='utf-8') as f:
            print(f"  📄 Created file: {filename}")
            print(f"  ⏱️  You can open this file now to watch progress in real-time!\n")
            
            # Write header
            f.write(f"# {chapter}\n\n")
            f.write(f"## Section {section_num}: {section_title}\n\n")
            f.write(f"*Generation started: {time.strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
            f.write("---\n\n")
            f.flush()
            
            # Step 1: Expand to topics
            print(f"  [1/4] 🔍 Planning content structure...")
            topics = expand_section_to_topics(generator, section_title)
            
            # Step 2: Expand topics to subsections
            for topic in topics:
                subsections = expand_topic_to_subsections(generator, section_title, topic)
                topic.subsections = subsections
            print(f"        ✅ Structure ready ({len(topics)} topics, {sum(len(t.subsections) for t in topics)} subsections)")
            
            # Step 3: Write content
            print(f"  [3/4] ✍️  Writing content (this will take time)...\n")
            
            # Introduction
            print(f"      📝 Writing introduction...")
            intro = write_section_introduction(generator, section_title, topics)
            f.write(intro + "\n\n")
            f.flush()
            word_count = len(intro.split())
            print(f"         ✅ Introduction complete (~{len(intro.split())} words)")
            
            # Write each topic and its subsections
            for topic_idx, topic in enumerate(topics, 1):
                print(f"\n      📚 Topic {topic_idx}/{len(topics)}: {topic.title}")
                f.write(f"### {section_num}.{topic_idx} {topic.title}\n\n")
                f.flush()
                
                for subsection_idx, subsection in enumerate(topic.subsections, 1):
                    print(f"         ✏️  Writing: {subsection}...", end=" ")
                    
                    subsection_content = write_subsection(
                        generator,
                        section_title,
                        topic.title,
                        subsection,
                        target_words=1000
                    )
                    
                    f.write(f"#### {section_num}.{topic_idx}.{subsection_idx} {subsection}\n\n")
                    f.write(subsection_content + "\n\n")
                    f.flush()
                    
                    word_count += len(subsection_content.split())
                    print(f"✅ (~{len(subsection_content.split())} words, total: {word_count})")
            
            # Summary
            print(f"\n      📝 Writing summary and reflection...")
            summary = write_section_summary(generator, section_title, topics)
            f.write(f"### Summary and Reflection\n\n")
            f.write(summary + "\n\n")
            f.flush()
            word_count += len(summary.split())
            print(f"         ✅ Summary complete (~{len(summary.split())} words)")
            
            # Footer
            f.write("\n---\n\n")
            f.write(f"*Generation completed: {time.strftime('%Y-%m-%d %H:%M:%S')}*\n")
            f.write(f"*Total words: ~{word_count}*\n")
            f.flush()
        
        print(f"\n  [4/4] ✅ Section {section_num} complete!")
        print(f"        📊 Total words: ~{word_count}")
        print(f"        📁 Saved to: {filename}\n")
    
    # STEP 3: Combine all sections
    print(f"\n{'='*70}")
    print("STEP 3: Combining All Sections into Final Document")
    print(f"{'='*70}\n")
    
    combined_content = f"# Complete Textbook\n\n"
    combined_content += f"*Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
    combined_content += "---\n\n"
    
    total_words = 0
    for idx, section_info in enumerate(sections, 1):
        section_num = section_info['section_number']
        section_title = section_info['section_title']
        filename = f"output/Section_{section_num}_{section_title.replace(' ', '_')}.md"
        
        print(f"  [{idx}/{len(sections)}] Adding Section {section_num}...")
        
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            combined_content += content + "\n\n"
            total_words += len(content.split())
    
    # Save combined document
    combined_filename = "output/Complete_Textbook.md"
    with open(combined_filename, 'w', encoding='utf-8') as f:
        f.write(combined_content)
    
    print(f"\n{'='*70}")
    print("✅ GENERATION COMPLETE!")
    print(f"{'='*70}\n")
    print(f"📚 Total sections: {len(sections)}")
    print(f"📊 Total words: ~{total_words:,}")
    print(f"📁 Complete textbook: {combined_filename}")
    print(f"📁 Master Commands: output/master_commands/")
    print(f"\n🎉 All done!\n")

if __name__ == "__main__":
    generate_textbook_multistep()
