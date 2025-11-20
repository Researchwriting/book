"""
Interactive Textbook Generator - User-controlled generation
"""
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.config import Config
from src.generator import get_generator
from src.syllabus_parser import parse_syllabus
from src.master_command_generator import generate_master_command
from src.textbook_planner import expand_section_to_topics, expand_topic_to_subsections
from src.textbook_writer import write_section_introduction, write_subsection, write_section_summary
from src.outline_input import interactive_outline_input
from src.quality_control import check_quality, print_quality_report
from src.cost_tracker import cost_tracker
from src.export_manager import auto_export_all
from src.resume_manager import resume_manager
from src.parallel_generator import ParallelGenerator
from src.model_switcher import switch_model, get_current_model, compare_costs
from src.auto_notifier import AutoNotifier, load_notification_config
from src.progress_tracker import progress_tracker

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def print_header(config):
    print("=" * 70)
    print("🎓 INTERACTIVE TEXTBOOK GENERATOR")
    print(f"   Model: {get_current_model(config)}")
    print("=" * 70)
    print()

def show_menu(sections, config):
    print("\n📚 Available Sections:\n")
    for idx, section_info in enumerate(sections, 1):
        section_num = section_info['section_number']
        section_title = section_info['section_title']
        
        # Check if already generated
        filename = f"output/Section_{section_num}_{section_title.replace(' ', '_')}.md"
        status = "✅ DONE" if os.path.exists(filename) else "⏳ PENDING"
        
        print(f"  [{idx}] Section {section_num}: {section_title}")
        print(f"      Status: {status}")
        print()
    
    # Show cost summary
    summary = cost_tracker.get_summary()
    if summary['total_tokens'] > 0:
        print(f"\n💰 Cost so far: ${summary['cost_usd']:.4f} ({summary['total_tokens']:,} tokens)")
    
    print("\n" + "=" * 70)
    print("\n📋 Options:")
    print("  [1-11]  Generate a specific section")
    print("  [a]     Generate ALL sections (sequential)")
    print("  [p]     Generate ALL sections (PARALLEL - 2x faster)  ← NEW!")
    print("  [m]     View Master Commands")
    print("  [s]     Show status")
    print("  [n]     Enter NEW outline")
    print("  [e]     Export to DOCX/PDF")
    print("  [c]     Show cost summary")
    print("  [x]     Switch AI model (DeepSeek ⇄ Gemini)  ← NEW!")
    print("  [q]     Quit")
    print("\n" + "=" * 70)

def generate_section(generator, section_info, section_idx, total_sections):
    chapter = section_info['chapter']
    section_num = section_info['section_number']
    section_title = section_info['section_title']
    
    print(f"\n{'='*70}")
    print(f"📝 Generating Section {section_idx}/{total_sections}: {section_title}")
    print(f"{'='*70}\n")
    
    # Check if section can be resumed
    resume_point = resume_manager.get_resume_point(section_num)
    if resume_point:
        print(f"⚠️  Found partial progress for this section!")
        print(f"   Completed: {len(resume_point['completed_subsections'])} subsections")
        response = input("\n[r] Resume from where you left off\n[s] Start fresh (delete progress)\n[c] Cancel\n\nYour choice: ").strip().lower()
        
        if response == 'c':
            print("❌ Cancelled.")
            return
        elif response == 's':
            resume_manager.clear_section(section_num)
            resume_point = None
            print("✅ Progress cleared. Starting fresh...")
        else:
            print("✅ Resuming from last checkpoint...")
    
    # Create output file
    filename = f"output/Section_{section_num}_{section_title.replace(' ', '_')}.md"
    
    # Check if file exists and no resume point
    if os.path.exists(filename) and not resume_point:
        print(f"⚠️  Section already exists: {filename}")
        response = input("\nOverwrite? (y/n): ").strip().lower()
        if response != 'y':
            print("❌ Cancelled.")
            return
    
    # Open file for real-time writing
    with open(filename, 'w', encoding='utf-8') as f:
        print(f"  📄 Created file: {filename}")
        print(f"  ⏱️  You can open this file now to watch progress!\n")
        
        # Write header
        f.write(f"# {chapter}\n\n")
        f.write(f"## Section {section_num}: {section_title}\n\n")
        f.write(f"*Generation started: {time.strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        f.write("---\n\n")
        f.flush()
        
        
        # Step 1: Expand to topics
        print(f"  [1/4] 🔍 Planning content structure...")
        print(f"        🤖 AI is analyzing '{section_title}' and creating topics...")
        start_time = time.time()
        topics = expand_section_to_topics(generator, section_title)
        elapsed = time.time() - start_time
        
        # Mark section as started
        resume_manager.start_section(section_num, section_title, len(topics))
        
        # Step 2: Expand topics to subsections
        print(f"        🤖 AI is creating subsections for each topic...")
        for topic in topics:
            subsections = expand_topic_to_subsections(generator, section_title, topic)
            topic.subsections = subsections
        total_subsections = sum(len(t.subsections) for t in topics)
        print(f"        ✅ Structure ready ({len(topics)} topics, {total_subsections} subsections) - took {int(elapsed)}s")
        
        # Initialize Progress Tracker
        progress_tracker.start_section(section_num, section_title, total_subsections + 2)

        
        # Step 3: Write content
        print(f"  [2/4] ✍️  Writing content...\n")
        
        # Calculate total work
        total_subsections = sum(len(t.subsections) for t in topics) + 2  # +2 for intro and summary
        completed_subsections = 0
        section_start_time = time.time()
        
        # Introduction
        print(f"      📝 [0/{total_subsections}] Writing introduction...")
        
        # Update Progress Tracker
        progress_tracker.update_subsection(section_num, "Introduction")
        
        intro = write_section_introduction(generator, section_title, topics)
        f.write(intro + "\n\n")
        f.flush()
        word_count = len(intro.split())
        completed_subsections += 1
        
        # Update Progress Tracker
        progress_tracker.complete_subsection(section_num, word_count)
        
        elapsed = time.time() - section_start_time
        avg_time_per_part = elapsed / completed_subsections
        remaining_parts = total_subsections - completed_subsections
        est_remaining = int(avg_time_per_part * remaining_parts / 60)
        print(f"         ✅ Introduction complete (~{len(intro.split())} words) | Progress: {int(completed_subsections/total_subsections*100)}% | Est. remaining: ~{est_remaining}min")
        
        # Write each topic and its subsections
        
        for topic_idx, topic in enumerate(topics, 1):
            print(f"\n      📚 Topic {topic_idx}/{len(topics)}: {topic.title}")
            f.write(f"### {section_num}.{topic_idx} {topic.title}\n\n")
            f.flush()
            
            # Generate subsections in parallel (3 at a time for speed)
            def generate_single_subsection(subsection_idx, subsection):
                # Check if already completed
                if resume_manager.is_subsection_completed(section_num, topic_idx, subsection_idx):
                    return {
                        'idx': subsection_idx,
                        'title': subsection,
                        'content': None,
                        'skipped': True
                    }
                
                # Track input tokens
                prompt_estimate = f"{section_title} {topic.title} {subsection}"
                cost_tracker.estimate_tokens(prompt_estimate, is_input=True)
                
                # Generate content
                subsection_content = write_subsection(
                    generator,
                    section_title,
                    topic.title,
                    subsection,
                    target_words=1000
                )
                
                # Track output tokens
                cost_tracker.estimate_tokens(subsection_content, is_input=False)
                
                return {
                    'idx': subsection_idx,
                    'title': subsection,
                    'content': subsection_content,
                    'skipped': False
                }
            
            
            # Generate subsections in parallel
            # Use 10 workers for Gemini Flash (ultra-fast), 3 for others
            from src.config import LLMProvider
            max_workers = 10 if hasattr(generator, 'model_name') and 'flash' in generator.model_name.lower() else 3
            
            subsection_results = []
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {
                    executor.submit(generate_single_subsection, idx, sub): (idx, sub)
                    for idx, sub in enumerate(topic.subsections, 1)
                }
                
                # Collect results as they complete
                for future in as_completed(futures):
                    idx, subsection = futures[future]
                    try:
                        result = future.result()
                        subsection_results.append(result)
                        
                        if result['skipped']:
                            print(f"         ⏭️  [{completed_subsections}/{total_subsections}] Skipped: {result['title']}")
                        else:
                            word_count += len(result['content'].split())
                            completed_subsections += 1
                            
                            # Update time estimate
                            elapsed = time.time() - section_start_time
                            avg_time_per_part = elapsed / completed_subsections
                            remaining_parts = total_subsections - completed_subsections
                            est_remaining = int(avg_time_per_part * remaining_parts / 60)
                            progress_pct = int(completed_subsections/total_subsections*100)
                            
                            # Update Progress Tracker
                            progress_tracker.update_subsection(section_num, result['title'])
                            progress_tracker.complete_subsection(section_num, len(result['content'].split()))
                            
                            print(f"         ✅ [{completed_subsections}/{total_subsections}] {result['title'][:50]}... ({len(result['content'].split())} words) | {progress_pct}% | ~{est_remaining}min left")
                    
                    except Exception as e:
                        print(f"\n❌ Error generating subsection: {e}")
                        raise
            
            # Sort results by index and write to file in order
            subsection_results.sort(key=lambda x: x['idx'])
            for result in subsection_results:
                if not result['skipped']:
                    f.write(f"#### {section_num}.{topic_idx}.{result['idx']} {result['title']}\n\n")
                    f.write(result['content'] + "\n\n")
                    f.flush()
                    
                    # Mark as completed
                    resume_manager.complete_subsection(section_num, topic_idx, result['idx'])
            
            # Mark topic as completed
            resume_manager.complete_topic(section_num, topic_idx)
        
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
    
    # Mark section as completed
    resume_manager.complete_section(section_num)
    
    print(f"\n  [4/4] ✅ Section {section_num} complete!")
    print(f"        📊 Total words: ~{word_count}")
    print(f"        📁 Saved to: {filename}\n")
    
    # Auto-convert to DOCX
    print(f"  [5/5] 📄 Creating professional DOCX...")
    try:
        from src.docx_generator import auto_convert_to_docx
        docx_file = auto_convert_to_docx(filename)
        if docx_file:
            print(f"        ✅ DOCX created: {docx_file}")
    except ImportError:
        print(f"        ⚠️  Install python-docx: pip install python-docx")
    except Exception as e:
        print(f"        ⚠️  DOCX conversion failed: {e}")
    
    # Auto-notification
    notifier_config = load_notification_config()
    if notifier_config:
        notifier = AutoNotifier(notifier_config)
        notifier.notify_section_complete(filename, section_num, section_title)
    
    input("\nPress Enter to continue...")

def main():
    config = Config()
    generator = get_generator(config)
    
    # Create output directories
    os.makedirs("output", exist_ok=True)
    os.makedirs("output/master_commands", exist_ok=True)
    
    # Check if outline exists, if not prompt for input
    if not os.path.exists("syllabus.md"):
        print("\n⚠️  No syllabus.md found!")
        if not interactive_outline_input():
            print("\n❌ Cannot proceed without an outline. Exiting.")
            sys.exit(1)
    
    # Parse syllabus
    syllabus_path = "syllabus.md"
    sections = parse_syllabus(syllabus_path)
    
    # Generate Master Commands (if not already done)
    print("🔧 Checking Master Commands...")
    for section_info in sections:
        section_num = section_info['section_number']
        mc_filename = f"output/master_commands/Section_{section_num}_Master_Command.md"
        
        if not os.path.exists(mc_filename):
            master_command = generate_master_command(section_info)
            with open(mc_filename, 'w', encoding='utf-8') as f:
                f.write(master_command)
    
    print("✅ Master Commands ready!\n")
    
    while True:
        clear_screen()
        print_header(config)
        show_menu(sections, config)
        
        choice = input("\nYour choice: ").strip().lower()
        
        if choice == 'q':
            print("\n👋 Goodbye!")
            sys.exit(0)
        
        elif choice == 'x':
            print("\n🔄 Switch AI Model")
            print("\nCurrent model:", get_current_model(config))
            print("\nAvailable models:")
            print("  [1] DeepSeek (cheapest, good quality)")
            print("  [2] Gemini (cheapest, fast)")
            print("  [3] Show cost comparison")
            
            model_choice = input("\nYour choice: ").strip()
            
            if model_choice == '1':
                config = switch_model('deepseek')
                generator = get_generator(config)
            elif model_choice == '2':
                config = switch_model('gemini')
                generator = get_generator(config)
            elif model_choice == '3':
                compare_costs()
            
            input("\nPress Enter to continue...")
        
        elif choice == 'n':
            print("\n📝 Entering new outline...")
            if interactive_outline_input():
                print("\n✅ Outline updated! Reloading...")
                sections = parse_syllabus(syllabus_path)
                # Regenerate Master Commands
                for section_info in sections:
                    section_num = section_info['section_number']
                    mc_filename = f"output/master_commands/Section_{section_num}_Master_Command.md"
                    master_command = generate_master_command(section_info)
                    with open(mc_filename, 'w', encoding='utf-8') as f:
                        f.write(master_command)
            input("\nPress Enter to continue...")
        
        
        elif choice == 'a':
            print("\n⚠️  This will generate ALL sections sequentially (~3-4 hours)")
            confirm = input("Continue? (y/n): ").strip().lower()
            if confirm == 'y':
                for idx, section_info in enumerate(sections, 1):
                    generate_section(generator, section_info, idx, len(sections))
        
        elif choice == 'p':
            print("\n⚡ PARALLEL GENERATION")
            print(f"\nThis will generate ALL {len(sections)} sections in parallel (2 at a time)")
            print(f"Estimated time: ~{len(sections) * 25 // 2} minutes")
            confirm = input("\nContinue? (y/n): ").strip().lower()
            if confirm == 'y':
                from concurrent.futures import ThreadPoolExecutor, as_completed
                
                print("\n🚀 Starting parallel generation...\n")
                
                with ThreadPoolExecutor(max_workers=2) as executor:
                    futures = {
                        executor.submit(generate_section, generator, section_info, idx, len(sections)): section_info
                        for idx, section_info in enumerate(sections, 1)
                    }
                    
                    completed = 0
                    total = len(sections)
                    
                    for future in as_completed(futures):
                        section_info = futures[future]
                        completed += 1
                        try:
                            future.result()
                            print(f"\n✅ [{completed}/{total}] Section {section_info['section_number']} complete!")
                        except Exception as e:
                            print(f"\n❌ [{completed}/{total}] Section {section_info['section_number']} failed: {e}")
                
                print("\n🎉 All sections complete!")
                input("\nPress Enter to continue...")
        
        
        elif choice == 'm':
            print("\n📁 Master Commands:")
            for section_info in sections:
                section_num = section_info['section_number']
                section_title = section_info['section_title']
                mc_filename = f"output/master_commands/Section_{section_num}_Master_Command.md"
                print(f"  Section {section_num}: {mc_filename}")
            input("\nPress Enter to continue...")
        
        elif choice == 's':
            print("\n📊 Generation Status:")
            total = len(sections)
            done = 0
            for section_info in sections:
                section_num = section_info['section_number']
                section_title = section_info['section_title']
                filename = f"output/Section_{section_num}_{section_title.replace(' ', '_')}.md"
                
                if os.path.exists(filename):
                    done += 1
                    # Get word count
                    with open(filename, 'r') as f:
                        words = len(f.read().split())
                    print(f"  ✅ Section {section_num}: {section_title} (~{words} words)")
                else:
                    print(f"  ⏳ Section {section_num}: {section_title} (pending)")
            
            print(f"\n  Progress: {done}/{total} sections complete")
            input("\nPress Enter to continue...")
        
        elif choice == 'e':
            print("\n📦 Exporting to DOCX/PDF...")
            auto_export_all()
            input("\nPress Enter to continue...")
        
        elif choice == 'c':
            print("\n")
            cost_tracker.print_summary()
            input("\nPress Enter to continue...")
        
        elif choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(sections):
                generate_section(generator, sections[idx-1], idx, len(sections))
            else:
                print(f"\n❌ Invalid section number. Choose 1-{len(sections)}")
                input("\nPress Enter to continue...")
        
        else:
            print("\n❌ Invalid choice. Try again.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
        sys.exit(0)
