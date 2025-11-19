#!/usr/bin/env python3
"""
Universal Content Generator - One script for everything
Asks user what they want and generates it
"""
import os
import sys

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def main_menu():
    clear_screen()
    print("=" * 70)
    print("🎓 UNIVERSAL CONTENT GENERATOR")
    print("=" * 70)
    print("\nWhat would you like to generate?\n")
    print("  [1] Short Essay (2,000-5,000 words)")
    print("  [2] Long Essay/Article (5,000-10,000 words)")
    print("  [3] Single Chapter (40,000-50,000 words)")
    print("  [4] Full Textbook (400,000+ words)")
    print("  [5] Custom (specify your own word count)")
    print("\n  [q] Quit")
    print("\n" + "=" * 70)
    
    choice = input("\nYour choice: ").strip().lower()
    return choice

def get_topic():
    print("\n" + "=" * 70)
    print("📝 TOPIC SETUP")
    print("=" * 70)
    topic = input("\nWhat's your topic/title? ").strip()
    return topic

def get_custom_words():
    while True:
        try:
            words = int(input("\nHow many words do you want? "))
            if words > 0:
                return words
            print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")

def get_context():
    print("\n" + "=" * 70)
    print("🌍 CONTEXT (Optional)")
    print("=" * 70)
    print("\nExamples: African context, Western context, Asian context, etc.")
    context = input("Context (press Enter to skip): ").strip()
    return context if context else "general academic"

def generate_content(content_type, topic, word_count, context):
    """Generate content based on user specifications."""
    from src.config import Config
    from src.generator import get_generator
    
    # Setup
    config = Config()
    generator = get_generator(config)
    
    # Create output directory
    os.makedirs("output", exist_ok=True)
    
    # Sanitize filename
    safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_topic = safe_topic.replace(' ', '_')
    filename = f"output/{safe_topic}.md"
    
    # Generate based on word count
    if word_count <= 5000:
        # Short essay - single piece
        clear_screen()
        print("=" * 70)
        print(f"🚀 GENERATING: {topic}")
        print("=" * 70)
        print(f"\nType: {content_type}")
        print(f"Target: {word_count:,} words")
        print(f"Context: {context}")
        print("\nThis will take approximately:", end=" ")
        
        # Estimate time
        minutes = word_count // 200  # ~200 words per minute
        if minutes < 5:
            print(f"{minutes} minutes")
        elif minutes < 60:
            print(f"{minutes} minutes")
        else:
            hours = minutes / 60
            print(f"{hours:.1f} hours")
        
        print("\n" + "=" * 70)
        confirm = input("\nStart generation? (y/n): ").strip().lower()
        if confirm != 'y':
            print("\n❌ Cancelled")
            return
        print(f"\n📄 Creating: {filename}\n")
        generate_essay(generator, topic, word_count, context, filename)
    elif word_count <= 10000:
        # Long essay - 3 sections
        clear_screen()
        print("=" * 70)
        print(f"🚀 GENERATING: {topic}")
        print("=" * 70)
        print(f"\nType: {content_type}")
        print(f"Target: {word_count:,} words")
        print(f"Context: {context}")
        print("\nThis will take approximately:", end=" ")
        
        # Estimate time
        minutes = word_count // 200  # ~200 words per minute
        if minutes < 5:
            print(f"{minutes} minutes")
        elif minutes < 60:
            print(f"{minutes} minutes")
        else:
            hours = minutes / 60
            print(f"{hours:.1f} hours")
        
        print("\n" + "=" * 70)
        confirm = input("\nStart generation? (y/n): ").strip().lower()
        if confirm != 'y':
            print("\n❌ Cancelled")
            return
        print(f"\n📄 Creating: {filename}\n")
        generate_long_essay(generator, topic, word_count, context, filename)
    elif word_count <= 50000:
        # Chapter - use section generator (no confirmation here, it has its own)
        generate_chapter(generator, topic, word_count, context, filename)
        return  # Return early, chapter handles its own completion message
    else:
        # Full textbook - use interactive main
        print("For textbooks >50,000 words, please use:")
        print("python3 -m src.interactive_main")
        return
    
    print("\n" + "=" * 70)
    print("✅ GENERATION COMPLETE!")
    print("=" * 70)
    print(f"\n📁 Saved to: {filename}")
    
    # Convert to DOCX
    try:
        from src.docx_generator import auto_convert_to_docx
        print("\n📄 Creating DOCX...")
        docx_file = auto_convert_to_docx(filename)
        if docx_file:
            print(f"✅ DOCX: {docx_file}")
    except:
        print("⚠️  DOCX conversion skipped (install python-docx)")
    
    # Email notification
    try:
        from src.auto_notifier import AutoNotifier, load_notification_config
        notifier_config = load_notification_config()
        if notifier_config and notifier_config.get('email_enabled'):
            print("\n📧 Sending email...")
            notifier = AutoNotifier(notifier_config)
            notifier.notify_section_complete(filename, "1", topic)
    except:
        pass
    
    print("\n✨ All done!\n")

def generate_essay(generator, topic, word_count, context, filename):
    """Generate a short essay (single cohesive piece)."""
    print("✍️  Generating essay...\n")
    
    prompt = f"""Write a comprehensive academic essay on the following topic:

TOPIC: {topic}

REQUIREMENTS:
- Length: Exactly {word_count} words
- Context: {context}
- Style: Academic, prose only (no bullet points)
- Structure: Introduction, body paragraphs, conclusion
- Include: Examples, analysis, critical thinking
- Tone: Teaching-focused, clear, professional
- Font: Times New Roman, 12pt (for DOCX)
- Spacing: 1.5 line spacing

Write the complete essay now:"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# {topic}\n\n")
        f.write(f"*Generated: {__import__('time').strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        f.write("---\n\n")
        
        # Generate in chunks for better quality
        chunks_needed = max(1, word_count // 1000)
        total_words = 0
        
        for i in range(chunks_needed):
            print(f"  Writing chunk {i+1}/{chunks_needed}...", end=" ")
            
            if i == 0:
                chunk_prompt = prompt
            else:
                chunk_prompt = f"Continue the essay on '{topic}'. Write the next {1000} words. Maintain the same academic tone and style."
            
            chunk = generator.generate(chunk_prompt, max_tokens=2000)
            f.write(chunk + "\n\n")
            f.flush()
            
            words = len(chunk.split())
            total_words += words
            print(f"✅ ({words} words, total: {total_words})")
        
        f.write("\n---\n\n")
        f.write(f"*Total words: ~{total_words}*\n")

def generate_long_essay(generator, topic, word_count, context, filename):
    """Generate a long essay (3 sections)."""
    print("✍️  Generating long essay with sections...\n")
    
    sections = [
        "Introduction and Background",
        "Main Analysis and Arguments",
        "Conclusion and Implications"
    ]
    
    words_per_section = word_count // 3
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# {topic}\n\n")
        f.write(f"*Generated: {__import__('time').strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        f.write("---\n\n")
        
        total_words = 0
        
        for i, section in enumerate(sections, 1):
            print(f"\n  Section {i}/3: {section}")
            f.write(f"## {section}\n\n")
            
            prompt = f"""Write section {i} of an essay on '{topic}'.

Section: {section}
Target: {words_per_section} words
Context: {context}
Style: Academic prose, no bullets

Write this section now:"""
            
            content = generator.generate(prompt, max_tokens=2000)
            f.write(content + "\n\n")
            f.flush()
            
            words = len(content.split())
            total_words += words
            print(f"    ✅ ({words} words)")
        
        f.write("\n---\n\n")
        f.write(f"*Total words: ~{total_words}*\n")

def generate_chapter(generator, topic, word_count, context, filename):
    """Generate a chapter using the full system with parallel processing."""
    print("✍️  Generating chapter with full outline...\n")
    
    # Ask for outline preference
    print("=" * 70)
    print("📋 CHAPTER OUTLINE")
    print("=" * 70)
    print("\nHow would you like to create the outline?\n")
    print("  [1] Auto-generate outline (AI creates sections for you)")
    print("  [2] Paste my own outline (you provide the sections)")
    print("\n" + "=" * 70)
    
    outline_choice = input("\nYour choice: ").strip()
    
    sections = []
    
    if outline_choice == '1':
        # Auto-generate outline
        print("\n🤖 Auto-generating outline...")
        print(f"Topic: {topic}")
        print(f"Context: {context}\n")
        
        num_sections = input("How many sections? (default: 10): ").strip()
        num_sections = int(num_sections) if num_sections else 10
        
        # Generate outline using AI
        outline_prompt = f"""Generate a detailed outline for a textbook chapter on "{topic}".

Context: {context}
Number of sections needed: {num_sections}

Generate {num_sections} section titles that cover this topic comprehensively.
Each section should be a clear, specific topic.

Format: Just list the section titles, one per line, numbered.
Example:
1. Introduction to the Topic
2. Historical Background
3. Core Concepts
...

Generate the outline now:"""
        
        outline_text = generator.generate(outline_prompt, max_tokens=500)
        
        print("\n✅ Generated outline:\n")
        print(outline_text)
        print("\n" + "=" * 70)
        
        confirm = input("\nUse this outline? (y/n): ").strip().lower()
        if confirm != 'y':
            print("\n❌ Cancelled")
            return
        
        # Parse generated outline
        for line in outline_text.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                section = re.sub(r'^\d+\.\s*', '', line)
                section = re.sub(r'^[-•]\s*', '', section)
                if section:
                    sections.append(section)
    
    elif outline_choice == '2':
        # Custom outline
        print("\n📋 Paste your chapter outline (one section per line):")
        print("Example:")
        print("  1. Surveys and Questionnaires")
        print("  2. Interviews: Structured, Semi-structured, Unstructured")
        print("  3. Focus Groups and Workshops")
        print("  ...")
        print("\nPaste now, then press Ctrl+D (Linux/Mac) or Ctrl+Z (Windows):\n")
        
        outline_lines = []
        try:
            while True:
                line = input()
                outline_lines.append(line)
        except EOFError:
            pass
        
        if not outline_lines:
            print("\n❌ No outline provided")
            return
        
        # Parse outline
        for line in outline_lines:
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                section = re.sub(r'^\d+\.\s*', '', line)
                section = re.sub(r'^[-•]\s*', '', line)
                if section:
                    sections.append(section)
    
    else:
        print("\n❌ Invalid choice")
        return
    
    if not sections:
        print("\n❌ No valid sections found in outline")
        return
    
    print(f"\n✅ Found {len(sections)} sections")
    print("\n" + "=" * 70)
    print("⚡ PARALLEL PROCESSING")
    print("=" * 70)
    print(f"\nThis will generate {len(sections)} sections in parallel (2 at a time)")
    print(f"Estimated time: ~{len(sections) * 20 // 2} minutes")
    print("\n" + "=" * 70)
    
    confirm = input("\nStart generation? (y/n): ").strip().lower()
    if confirm != 'y':
        print("\n❌ Cancelled")
        return
    
    # Create temporary outline file
    temp_outline = "temp_chapter_outline.md"
    with open(temp_outline, 'w') as f:
        f.write(f"# {topic}\n\n")
        for i, section in enumerate(sections, 1):
            f.write(f"## {i}. {section}\n")
    
    # Use the full system
    from src.syllabus_parser import parse_syllabus
    from src.master_command_generator import generate_master_command
    from src.textbook_planner import expand_section_to_topics, expand_topic_to_subsections
    from src.textbook_writer import write_section_introduction, write_subsection, write_section_summary
    from src.quality_control import check_quality, print_quality_report
    from src.cost_tracker import cost_tracker
    from src.resume_manager import resume_manager
    from src.output_organizer import output_organizer
    from src.progress_tracker import progress_tracker
    from src.auto_notifier import AutoNotifier, load_notification_config
    import time
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    # Parse
    parsed_sections = parse_syllabus(temp_outline)
    
    # Create organized output structure
    dirs = output_organizer.create_chapter_structure(topic)
    print(f"\n📁 Output directory: {dirs['chapter_dir']}")
    
    # Generate master commands
    print("🔧 Generating master commands...")
    for section_info in parsed_sections:
        section_num = section_info['section_number']
        mc_filename = output_organizer.get_master_command_path(topic, section_num)
        if not os.path.exists(mc_filename):
            master_command = generate_master_command(section_info)
            os.makedirs(os.path.dirname(mc_filename), exist_ok=True)
            with open(mc_filename, 'w', encoding='utf-8') as f:
                f.write(master_command)
    
    print("✅ Master commands ready!\n")
    
    # Start progress tracker
    print("🚀 Starting parallel generation with real-time progress...\n")
    print("⏳ Initializing progress tracker...")
    time.sleep(2)
    progress_tracker.start_display()
    
    # Generate sections in parallel
    def generate_single_section(section_info, idx, total, chapter_topic):
        """Generate a single section."""
        section_num = section_info['section_number']
        section_title = section_info['section_title']
        chapter = section_info['chapter']
        
        # Use organized path
        filename = output_organizer.get_section_path(chapter_topic, f"Section_{section_num}_{section_title}", 'md')
        
        # Check if already exists
        if os.path.exists(filename):
            return {'success': True, 'section_num': section_num, 'skipped': True}
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # Header
                f.write(f"# {chapter}\n\n")
                f.write(f"## Section {section_num}: {section_title}\n\n")
                f.write(f"*Generation started: {time.strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
                f.write("---\n\n")
                f.flush()
                
                # Expand to topics
                topics = expand_section_to_topics(generator, section_title)
                
                # Mark as started in progress tracker
                progress_tracker.start_section(section_num, section_title, len(topics) * 4)
                
                # Mark as started in resume manager
                resume_manager.start_section(section_num, section_title, len(topics))
                
                # Expand topics to subsections
                for topic in topics:
                    subsections = expand_topic_to_subsections(generator, section_title, topic)
                    topic.subsections = subsections
                
                # Write introduction
                progress_tracker.update_subsection(section_num, "Introduction")
                intro = write_section_introduction(generator, section_title, topics)
                f.write(intro + "\n\n")
                f.flush()
                word_count = len(intro.split())
                progress_tracker.complete_subsection(section_num, word_count)
                
                # Write subsections
                for topic_idx, topic in enumerate(topics, 1):
                    f.write(f"### {section_num}.{topic_idx} {topic.title}\n\n")
                    f.flush()
                    
                    for subsection_idx, subsection in enumerate(topic.subsections, 1):
                        if resume_manager.is_subsection_completed(section_num, topic_idx, subsection_idx):
                            continue
                        
                        # Update progress tracker
                        progress_tracker.update_subsection(section_num, subsection)
                        
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
                        
                        subsection_words = len(subsection_content.split())
                        word_count += subsection_words
                        
                        # Update progress
                        progress_tracker.complete_subsection(section_num, subsection_words)
                        resume_manager.complete_subsection(section_num, topic_idx, subsection_idx)
                    
                    resume_manager.complete_topic(section_num, topic_idx)
                
                # Write summary
                progress_tracker.update_subsection(section_num, "Summary and Reflection")
                summary = write_section_summary(generator, section_title, topics)
                f.write(f"### Summary and Reflection\n\n")
                f.write(summary + "\n\n")
                f.flush()
                summary_words = len(summary.split())
                word_count += summary_words
                progress_tracker.complete_subsection(section_num, summary_words)
                
                # Footer
                f.write("\n---\n\n")
                f.write(f"*Generation completed: {time.strftime('%Y-%m-%d %H:%M:%S')}*\n")
                f.write(f"*Total words: ~{word_count}*\n")
                f.flush()
            
            # Mark as completed
            resume_manager.complete_section(section_num)
            progress_tracker.complete_section(section_num, word_count)
            
            # Convert to DOCX
            try:
                from src.docx_generator import auto_convert_to_docx
                docx_path = output_organizer.get_section_path(chapter_topic, f"Section_{section_num}_{section_title}", 'docx')
                auto_convert_to_docx(filename)
                # Move DOCX to organized location
                temp_docx = filename.replace('.md', '.docx')
                if os.path.exists(temp_docx):
                    os.makedirs(os.path.dirname(docx_path), exist_ok=True)
                    os.rename(temp_docx, docx_path)
            except:
                pass
            
            # Email notification
            try:
                notifier_config = load_notification_config()
                if notifier_config and notifier_config.get('email_enabled'):
                    notifier = AutoNotifier(notifier_config)
                    notifier.notify_section_complete(filename, str(section_num), section_title)
            except Exception as e:
                # Don't let email failure stop the process
                pass
            
            return {'success': True, 'section_num': section_num, 'words': word_count}
        
        except Exception as e:
            return {'success': False, 'section_num': section_num, 'error': str(e)}
    
    # Run parallel generation
    print("🚀 Starting parallel generation (2 workers)...\n")
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {
            executor.submit(generate_single_section, section_info, idx, len(parsed_sections), topic): section_info
            for idx, section_info in enumerate(parsed_sections, 1)
        }
        
        completed = 0
        total = len(parsed_sections)
        
        for future in as_completed(futures):
            section_info = futures[future]
            result = future.result()
            completed += 1
            
            if result['success']:
                if result.get('skipped'):
                    print(f"⏭️  [{completed}/{total}] Section {result['section_num']} already exists")
                else:
                    print(f"✅ [{completed}/{total}] Section {result['section_num']} complete (~{result.get('words', 0)} words)")
            else:
                print(f"❌ [{completed}/{total}] Section {result['section_num']} failed: {result['error']}")
    
    # Stop progress tracker
    progress_tracker.stop_display()
    time.sleep(1)  # Give it time to stop
    
    # Clear screen and show final summary
    print("\033[2J\033[H")  # Clear screen
    
    # Combine all sections
    print("\n📚 Combining all sections...")
    combined_file = output_organizer.get_combined_path(topic, 'md')
    
    with open(combined_file, 'w', encoding='utf-8') as outfile:
        outfile.write(f"# {topic}\n\n")
        outfile.write(f"*Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        outfile.write("---\n\n")
        
        for section_info in parsed_sections:
            section_num = section_info['section_number']
            section_title = section_info['section_title']
            section_file = output_organizer.get_section_path(topic, f"Section_{section_num}_{section_title}", 'md')
            
            if os.path.exists(section_file):
                with open(section_file, 'r', encoding='utf-8') as infile:
                    content = infile.read()
                    # Skip the first header line
                    content = '\n'.join(content.split('\n')[1:])
                    outfile.write(content + "\n\n")
    
    print(f"✅ Combined file: {combined_file}")
    
    # Convert combined to DOCX
    try:
        from src.docx_generator import auto_convert_to_docx
        combined_docx = output_organizer.get_combined_path(topic, 'docx')
        auto_convert_to_docx(combined_file)
        # Move DOCX to organized location
        temp_docx = combined_file.replace('.md', '.docx')
        if os.path.exists(temp_docx):
            os.rename(temp_docx, combined_docx)
            print(f"✅ Combined DOCX: {combined_docx}")
    except:
        pass
    
    # Clean up
    if os.path.exists(temp_outline):
        os.remove(temp_outline)
    
    return combined_file

import re


def main():
    while True:
        choice = main_menu()
        
        if choice == 'q':
            print("\n👋 Goodbye!")
            sys.exit(0)
        
        elif choice == '1':
            topic = get_topic()
            context = get_context()
            generate_content("Short Essay", topic, 2000, context)
            input("\nPress Enter to continue...")
        
        elif choice == '2':
            topic = get_topic()
            context = get_context()
            generate_content("Long Essay", topic, 7500, context)
            input("\nPress Enter to continue...")
        
        elif choice == '3':
            topic = get_topic()
            context = get_context()
            generate_content("Single Chapter", topic, 45000, context)
            input("\nPress Enter to continue...")
        
        elif choice == '4':
            print("\n⚠️  For full textbooks, please use:")
            print("python3 -m src.interactive_main")
            input("\nPress Enter to continue...")
        
        elif choice == '5':
            topic = get_topic()
            word_count = get_custom_words()
            context = get_context()
            generate_content("Custom Content", topic, word_count, context)
            input("\nPress Enter to continue...")
        
        else:
            print("\n❌ Invalid choice")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Stop progress tracker if running
        try:
            from src.progress_tracker import progress_tracker
            progress_tracker.stop_display()
        except:
            pass
        print("\n\n👋 Interrupted by user. Goodbye!")
        import sys
        sys.exit(0)
