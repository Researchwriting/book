import os
import time
from .structure import ThesisStructure
from .writer import ThesisWriter
from .config import Config
from .state_manager import ThesisStateManager
from .planner import ChapterPlanner
from .reference_manager import ReferenceManager
from .instrument_designer import InstrumentDesigner
from .llm import LLMClient
from .chapter5_generator import Chapter5DiscussionGenerator
from .chapter6_generator import Chapter6Generator
from .analysis.data_analysis_orchestrator import DataAnalysisOrchestrator
from .chapter4_planner import Chapter4Planner

# Email and DOCX support
try:
    from .email_notifier import EmailNotifier
    from .docx_formatter import ThesisDocxFormatter
    EMAIL_DOCX_AVAILABLE = True
except ImportError:
    EMAIL_DOCX_AVAILABLE = False
    print("⚠️  Email/DOCX features not available. Install python-docx to enable.")

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def print_header():
    print("=" * 70)
    print("🎓 PhD UoJ THESIS GENERATOR")
    print("=" * 70)
    print()

def main():
    clear_screen()
    print_header()
    
    print("Please provide the details for your thesis:\n")
    topic = input("Enter Research Topic: ").strip()
    case_study = input("Enter Case Study (e.g., 'South Sudan'): ").strip()
    
    if not topic or not case_study:
        print("Error: Topic and Case Study are required.")
        return

    print("\nSelect Generation Mode:")
    print("  [1] Generate Full Thesis (All Chapters)")
    print("  [2] Generate Specific Chapter")
    mode = input("\nYour choice: ").strip()
    
    target_chapter = None
    if mode == '2':
        print("\nSelect Chapter:")
        print("  [1] Chapter One: Introduction")
        print("  [2] Chapter Two: Literature Review")
        print("  [3] Chapter Three: Methodology")
        print("  [4] Chapter Four: Data Presentation")
        print("  [5] Chapter Five: Results & Discussion")
        print("  [6] Chapter Six: Conclusion")
        ch_choice = input("\nYour choice: ").strip()
        chapter_map = {
            '1': "CHAPTER ONE", '2': "CHAPTER TWO", '3': "CHAPTER THREE",
            '4': "CHAPTER FOUR", '5': "CHAPTER FIVE", '6': "CHAPTER SIX"
        }
        target_chapter = chapter_map.get(ch_choice)
        if not target_chapter:
            print("Invalid chapter selected.")
            return

    print(f"\n🚀 Starting generation for: {topic}")
    print(f"📍 Case Study: {case_study}")
    print("=" * 70)
    
    
    state_manager = ThesisStateManager(topic=topic)
    reference_manager = ReferenceManager(topic=topic)
    planner = ChapterPlanner()
    writer = ThesisWriter(state_manager, reference_manager)
    llm_client = LLMClient()
    ch5_generator = Chapter5DiscussionGenerator(llm_client, state_manager)
    ch6_generator = Chapter6Generator(llm_client, state_manager)
    structure = ThesisStructure.get_structure()
    
    # Initialize email notifier if enabled
    email_notifier = None
    if EMAIL_DOCX_AVAILABLE and Config.EMAIL_ENABLED:
        if Config.EMAIL_ADDRESS and Config.EMAIL_PASSWORD and Config.RECIPIENT_EMAIL:
            email_notifier = EmailNotifier(
                Config.EMAIL_ADDRESS,
                Config.EMAIL_PASSWORD,
                Config.RECIPIENT_EMAIL
            )
            print("📧 Email notifications enabled")
        else:
            print("⚠️  Email enabled but credentials not configured in config.py")
    
    # Initialize DOCX formatter if available
    docx_formatter = ThesisDocxFormatter() if EMAIL_DOCX_AVAILABLE else None
    
    # Create output directory
    os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
    filename = f"{Config.OUTPUT_DIR}/Thesis_{topic.replace(' ', '_')[:30]}.md"
    
    # Open in append mode if generating single chapter, else write
    mode_flag = 'a' if target_chapter else 'w'
    
    with open(filename, mode_flag, encoding='utf-8') as f:
        if not target_chapter:
            # Write Title Page (Simplified)
            f.write(f"# {topic}\n\n")
            f.write(f"**Case Study:** {case_study}\n\n")
            f.write("A Thesis Submitted to the University of Juba\n")
            f.write("GRADUATE COLLEGE\n\n")
            f.write("---\n\n")
        
        for i, (chapter_key, chapter_data) in enumerate(structure.items(), 1):
            # Skip if we are targeting a specific chapter and this isn't it
            if target_chapter and chapter_key != target_chapter:
                continue
                
            print(f"\n📚 Processing {chapter_key}: {chapter_data['title']}")
            
            # SPECIAL HANDLING FOR CHAPTER 5
            if chapter_key == "CHAPTER FIVE":
                objectives = state_manager.get_section_content("CHAPTER ONE", "1.4 Objectives")
                content = ch5_generator.generate_chapter5(objectives, topic, case_study)
                f.write(content + "\n\n")
                state_manager.save_section(chapter_key, "Full Chapter", content)
                print(f"✅ {chapter_key} Complete!")
                continue
            
            # SPECIAL HANDLING FOR CHAPTER FOUR - Use DataAnalysisOrchestrator
            if chapter_key == "CHAPTER FOUR":
                print("\n📊 Generating Chapter 4 using real data analysis...")
                
                # Get objectives and methodology from previous chapters
                objectives = state_manager.get_section_content("CHAPTER ONE", "1.4 Objectives") or ""
                methodology = state_manager.get_section_content("CHAPTER THREE", "3.3 Research Design") or ""
                research_questions = state_manager.get_section_content("CHAPTER ONE", "1.5 Research questions/hypothesis") or ""
                
                # Initialize Chapter 4 planner and orchestrator
                ch4_planner = Chapter4Planner(llm_client, state_manager)
                data_orchestrator = DataAnalysisOrchestrator(planner=ch4_planner)
                
                # Generate Chapter 4 with real data analysis
                f.write(f"# {chapter_key}\n")
                f.write(f"## {chapter_data['title']}\n\n")
                
                content = data_orchestrator.analyze_all_data(
                    objectives=objectives,
                    methodology=methodology,
                    research_questions=research_questions
                )
                
                f.write(content + "\n\n")
                state_manager.save_section(chapter_key, "Full Chapter", content)
                print(f"✅ {chapter_key} Complete!")
                continue
                
            # SPECIAL HANDLING FOR CHAPTER SIX
            if chapter_key == "CHAPTER SIX":
                objectives = state_manager.get_section_content("CHAPTER ONE", "1.4 Objectives")
                content = ch6_generator.generate_chapter6(objectives, topic, case_study)
                f.write(content + "\n\n")
                state_manager.save_section(chapter_key, "Full Chapter", content)
                print(f"✅ {chapter_key} Complete!")
                continue
            
            # Generate custom outline for this chapter
            custom_outline = planner.plan_chapter(chapter_key, chapter_data['title'], topic, case_study)
            
            f.write(f"# {chapter_key}\n")
            f.write(f"## {chapter_data['title']}\n\n")
            
            # Track review files for this chapter
            chapter_review_files = []
            
            # Use custom outline if available, otherwise use default sections
            sections_to_write = chapter_data['sections']
            
            for section in sections_to_write:
                print(f"   Writing section: {section}...")
                
                # Check if already generated in state
                existing_content = state_manager.state.get(chapter_key, {}).get(section)
                
                if existing_content and target_chapter:
                     print(f"   (Found existing content, re-generating as requested...)")
                
                # Check if this section has custom sub-sections
                subsections = custom_outline.get(section, [])
                
                if subsections:
                    print(f"   Using custom outline: {subsections}")
                    # Write main section header
                    f.write(f"### {section}\n\n")
                    
                    # Write each subsection
                    for subsection in subsections:
                        print(f"     - {subsection}...")
                        content = writer.write_section(chapter_data['title'], f"{section} - {subsection}", topic, case_study)
                        f.write(f"#### {subsection}\n\n")
                        f.write(content + "\n\n")
                        f.flush()
                    
                    # Save combined content to state
                    combined_content = f"[Custom outline with subsections: {', '.join(subsections)}]"
                    state_manager.save_section(chapter_key, section, combined_content)
                else:
                    # Standard section writing (Chapters 1, 2, 3 only)
                    content = writer.write_section(chapter_data['title'], section, topic, case_study)
                    
                    # Track review file for this section
                    review_file_path = f"thesis/reviews/Review_{chapter_key.replace(' ', '_')}_{section.replace(' ', '_').replace('/', '_')}.md"
                    if os.path.exists(review_file_path):
                        chapter_review_files.append(review_file_path)
                    
                    # Save to state
                    state_manager.save_section(chapter_key, section, content)
                    
                    f.write(f"### {section}\n\n")
                    f.write(content + "\n\n")
                    f.flush()
                
            
            # Combine all review files for this chapter
            combined_review_file = None
            if chapter_review_files:
                combined_review_file = f"thesis/reviews/Combined_Review_{chapter_key.replace(' ', '_')}.md"
                with open(combined_review_file, 'w', encoding='utf-8') as review_f:
                    review_f.write(f"# PEER REVIEW REPORT: {chapter_key}\n\n")
                    review_f.write(f"**Chapter**: {chapter_data['title']}\n")
                    review_f.write(f"**Total Sections Reviewed**: {len(chapter_review_files)}\n\n")
                    review_f.write("---\n\n")
                    
                    for review_file in chapter_review_files:
                        if os.path.exists(review_file):
                            with open(review_file, 'r', encoding='utf-8') as rf:
                                review_f.write(rf.read())
                                review_f.write("\n\n---\n\n")
                
                print(f"  📋 Combined {len(chapter_review_files)} review reports")
            
            print(f"✅ {chapter_key} Complete!")
            
            # Special: Generate research instrument after Chapter 3
            if chapter_key == "CHAPTER THREE":
                print("\n📋 Generating research instrument and simulated data...")
                
                # Get objectives and questions from Chapter 1
                objectives = state_manager.get_section_content("CHAPTER ONE", "1.4 Objectives")
                specific_obj = state_manager.get_section_content("CHAPTER ONE", "1.4.2 Specific objectives")
                questions = state_manager.get_section_content("CHAPTER ONE", "1.5 Research questions/hypothesis")
                
                objectives_combined = f"{objectives}\n\n{specific_obj}"
                
                # Initialize instrument designer
                llm = LLMClient()
                designer = InstrumentDesigner(llm)
                
                # Design instrument
                instrument = designer.design_instrument(
                    topic=topic,
                    case_study=case_study,
                    objectives=objectives_combined,
                    research_questions=questions,
                    methodology_type="quantitative"
                )
                
                # Save instrument
                instrument_file = designer.save_instrument(instrument)
                
                # Generate simulated data for Chapter 4
                simulated_data = designer.generate_simulated_data(
                    instrument=instrument,
                    sample_size=357,
                    topic=topic,
                    case_study=case_study
                )
                
                # Save simulated data
                data_file = designer.save_simulated_data(simulated_data)
                
                # Generate CSV/Excel datasets
                dataset_files = designer.generate_dataset(
                    instrument=instrument,
                    sample_size=357,
                    topic=topic,
                    case_study=case_study
                )
                
                print(f"  ✅ Instrument: {instrument_file}")
                print(f"  ✅ Data: {data_file}")
            
            print(f"✅ {chapter_key} Complete!\n")
            
            # Email chapter completion if enabled
            if email_notifier and not target_chapter:
                chapter_md = filename
                chapter_docx = None
                
                # Convert to DOCX if available
                if docx_formatter:
                    try:
                        chapter_docx = filename.replace('.md', f'_{chapter_key.replace(" ", "_")}.docx')
                        docx_formatter.markdown_to_docx(chapter_md, chapter_docx)
                    except Exception as e:
                        print(f"⚠️  DOCX conversion failed: {e}")
                
                # Send email with chapter content AND review report
                email_notifier.send_chapter_notification(
                    chapter_key, 
                    chapter_md, 
                    chapter_docx, 
                    combined_review_file  # Include combined review file
                )
        
        # After all chapters, convert full thesis to DOCX
        if docx_formatter and not target_chapter:
            try:
                print("\n📄 Converting full thesis to DOCX...")
                docx_output = filename.replace('.md', '.docx')
                docx_formatter.markdown_to_docx(filename, docx_output)
                print(f"✅ DOCX saved: {docx_output}")
            except Exception as e:
                print(f"⚠️  Full thesis DOCX conversion failed: {e}")
        
        # After all chapters, add bibliography
        print("\n📚 Generating bibliography...")
        all_refs = reference_manager.get_all_references()
        
        if all_refs:
            f.write("\n\n# BIBLIOGRAPHY\n\n")
            f.write("This section presents all references cited throughout the thesis, ")
            f.write("organised alphabetically by author surname.\n\n")
            
            # Sort references alphabetically by author
            sorted_refs = sorted(all_refs, key=lambda x: x.get('authors', ['Unknown'])[0] if isinstance(x.get('authors'), list) else 'Unknown')
            
            for ref in sorted_refs:
                bib_entry = reference_manager.format_reference(ref)
                f.write(f"{bib_entry}\n\n")
            
            print(f"  ✅ Added {len(all_refs)} references to bibliography")
        
        # Add appendices
        print("\n📎 Adding appendices...")
        f.write("\n\n# APPENDICES\n\n")
        
        # Appendix A: Research Instrument
        instrument_path = "thesis/appendices/Research_Instrument.md"
        if os.path.exists(instrument_path):
            with open(instrument_path, 'r', encoding='utf-8') as inst_file:
                instrument_content = inst_file.read()
                f.write(f"{instrument_content}\n\n")
            print("  ✅ Added Appendix A: Research Instrument")
        
        # Appendix B: Budget (if exists)
        budget_path = "thesis/appendices/Budget.md"
        if os.path.exists(budget_path):
            with open(budget_path, 'r', encoding='utf-8') as budget_file:
                f.write(budget_file.read() + "\n\n")
            print("  ✅ Added Appendix B: Budget")
        
        # Appendix C: Maps/Photos (if exist)
        maps_path = "thesis/appendices/Maps_Photos.md"
        if os.path.exists(maps_path):
            with open(maps_path, 'r', encoding='utf-8') as maps_file:
                f.write(maps_file.read() + "\n\n")
            print("  ✅ Added Appendix C: Maps and Photos")
    
    print(f"\n🎓 Thesis generation complete!")
    print(f"📄 Output: {filename}")
    
    # Generate bibliography
    print("\n📚 Generating bibliography...")
    bib_file = reference_manager.generate_bibliography()
    print(f"📚 Bibliography saved to: {bib_file}")
    
    input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
