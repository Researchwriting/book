#!/usr/bin/env python3
"""
Quick Test - Generate a tiny textbook to test the system
Target: 100 words per subsection (instead of 1000)
"""
import os
import sys
from src.config import Config
from src.generator import get_generator
from src.syllabus_parser import parse_syllabus
from src.textbook_planner import expand_section_to_topics, expand_topic_to_subsections
from src.textbook_writer import write_section_introduction, write_subsection, write_section_summary
from src.auto_notifier import AutoNotifier, load_notification_config
import time

def quick_test():
    print("\n" + "="*70)
    print("🧪 QUICK SYSTEM TEST")
    print("="*70)
    print("\nThis will generate a tiny test section (~500 words total)")
    print("Time: ~2-3 minutes")
    print("Purpose: Test all features (generation, quality checks, email, etc.)\n")
    
    confirm = input("Start test? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Cancelled")
        return
    
    # Setup
    config = Config()
    generator = get_generator(config)
    
    # Create test output directory
    os.makedirs("test_output", exist_ok=True)
    
    # Parse test outline
    sections = parse_syllabus("test_outline.md")
    
    if not sections:
        print("❌ No sections found in test_outline.md")
        return
    
    # Use first section only
    section_info = sections[0]
    section_num = section_info['section_number']
    section_title = section_info['section_title']
    
    print(f"\n📝 Generating Test Section: {section_title}")
    print("="*70 + "\n")
    
    filename = f"test_output/Test_Section_{section_num}.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        # Header
        f.write(f"# Test Chapter\n\n")
        f.write(f"## Section {section_num}: {section_title}\n\n")
        f.write(f"*Test generation started: {time.strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        f.write("---\n\n")
        f.flush()
        
        # Generate 2 topics (instead of 12)
        print("  [1/4] 🔍 Generating topics...")
        topics = expand_section_to_topics(generator, section_title, num_topics=2)
        print(f"        ✅ Generated {len(topics)} topics")
        
        # Generate 2 subsections per topic (instead of 4)
        print("  [2/4] 📋 Generating subsections...")
        for topic in topics:
            subsections = expand_topic_to_subsections(generator, section_title, topic, num_subsections=2)
            topic.subsections = subsections
        print(f"        ✅ Generated subsections")
        
        # Write introduction (short)
        print("  [3/4] ✍️  Writing content...\n")
        print("      📝 Writing introduction...")
        
        # Override to make it shorter
        intro_prompt = f"Write a 2-paragraph introduction (100 words) about {section_title}. Use prose only, no bullets."
        intro = generator.generate(intro_prompt, max_tokens=200)
        
        f.write(intro + "\n\n")
        f.flush()
        word_count = len(intro.split())
        print(f"         ✅ Introduction complete (~{word_count} words)")
        
        # Write subsections (100 words each)
        for topic_idx, topic in enumerate(topics, 1):
            print(f"\n      📚 Topic {topic_idx}/{len(topics)}: {topic.title}")
            f.write(f"### {section_num}.{topic_idx} {topic.title}\n\n")
            f.flush()
            
            for subsection_idx, subsection in enumerate(topic.subsections, 1):
                print(f"         ✏️  Writing: {subsection}...", end=" ")
                
                # Short subsection (100 words)
                subsection_prompt = f"""Write about "{subsection}" in the context of {section_title}.

RULES:
- Write exactly 100 words
- Use prose only (no bullet points)
- Include one simple ASCII diagram
- Teaching tone

Write now:"""
                
                subsection_content = generator.generate(subsection_prompt, max_tokens=300)
                
                f.write(f"#### {section_num}.{topic_idx}.{subsection_idx} {subsection}\n\n")
                f.write(subsection_content + "\n\n")
                f.flush()
                
                word_count += len(subsection_content.split())
                print(f"✅ (~{len(subsection_content.split())} words)")
        
        # Summary (short)
        print(f"\n      📝 Writing summary...")
        summary_prompt = f"Write a 2-paragraph summary (100 words) of {section_title}. Use prose only."
        summary = generator.generate(summary_prompt, max_tokens=200)
        
        f.write(f"### Summary\n\n")
        f.write(summary + "\n\n")
        f.flush()
        word_count += len(summary.split())
        print(f"         ✅ Summary complete (~{len(summary.split())} words)")
        
        # Footer
        f.write("\n---\n\n")
        f.write(f"*Test completed: {time.strftime('%Y-%m-%d %H:%M:%S')}*\n")
        f.write(f"*Total words: ~{word_count}*\n")
        f.flush()
    
    print(f"\n  [4/4] ✅ Test section complete!")
    print(f"        📊 Total words: ~{word_count}")
    print(f"        📁 Saved to: {filename}\n")
    
    # Test email notification
    notifier_config = load_notification_config()
    if notifier_config and notifier_config.get('email_enabled'):
        print("📧 Testing email notification...")
        notifier = AutoNotifier(notifier_config)
        notifier.notify_section_complete(filename, section_num, section_title)
    else:
        print("⚠️  Email not configured (run: python3 -m src.auto_notifier)")
    
    print("\n" + "="*70)
    print("✅ TEST COMPLETE!")
    print("="*70)
    print(f"\nCheck the file: {filename}")
    if notifier_config and notifier_config.get('email_enabled'):
        print(f"Check your email: {notifier_config.get('email_to')}")
    print("\nIf everything looks good, you can generate the full textbook!")
    print("Run: python3 -m src.interactive_main")

if __name__ == "__main__":
    quick_test()
