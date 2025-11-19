"""
Batch Processor - Generate multiple textbooks from multiple outline files
Optimized for SPEED, EFFICIENCY, and INTELLIGENCE
"""
import os
import glob
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.config import Config
from src.generator import get_generator
from src.syllabus_parser import parse_syllabus
from src.master_command_generator import generate_master_command
from src.interactive_main import generate_section
import time

class BatchProcessor:
    def __init__(self, max_workers: int = 3):
        """
        Initialize batch processor.
        
        Args:
            max_workers: Number of parallel workers (3 = 3x faster)
        """
        self.max_workers = max_workers
        self.results = {}
        self.errors = {}
    
    def find_outline_files(self, directory: str = ".") -> List[str]:
        """
        Find all outline files in directory.
        Looks for: syllabus*.md, outline*.md, chapter*.md
        """
        patterns = [
            f"{directory}/syllabus*.md",
            f"{directory}/outline*.md",
            f"{directory}/chapter*.md",
            f"{directory}/*_outline.md"
        ]
        
        files = []
        for pattern in patterns:
            files.extend(glob.glob(pattern))
        
        # Remove duplicates and sort
        files = sorted(list(set(files)))
        
        return files
    
    def process_single_outline(self, outline_file: str, config: Config) -> Dict:
        """
        Process a single outline file.
        
        Returns:
            Dict with status, sections_generated, errors
        """
        print(f"\n{'='*70}")
        print(f"📚 Processing: {outline_file}")
        print(f"{'='*70}\n")
        
        try:
            # Parse outline
            sections = parse_syllabus(outline_file)
            
            if not sections:
                return {
                    'status': 'error',
                    'error': 'No sections found in outline',
                    'sections_generated': 0
                }
            
            # Create output directory for this outline
            base_name = os.path.splitext(os.path.basename(outline_file))[0]
            output_dir = f"output/{base_name}"
            os.makedirs(output_dir, exist_ok=True)
            os.makedirs(f"{output_dir}/master_commands", exist_ok=True)
            
            print(f"📁 Output directory: {output_dir}")
            print(f"📊 Found {len(sections)} sections to generate\n")
            
            # Generate master commands
            for section_info in sections:
                section_num = section_info['section_number']
                mc_filename = f"{output_dir}/master_commands/Section_{section_num}_Master_Command.md"
                
                if not os.path.exists(mc_filename):
                    master_command = generate_master_command(section_info)
                    with open(mc_filename, 'w', encoding='utf-8') as f:
                        f.write(master_command)
            
            # Generate sections in parallel
            generator = get_generator(config)
            sections_generated = 0
            section_errors = []
            
            # Use ThreadPoolExecutor for parallel generation
            with ThreadPoolExecutor(max_workers=2) as executor:
                futures = {}
                
                for idx, section_info in enumerate(sections, 1):
                    section_num = section_info['section_number']
                    section_title = section_info['section_title']
                    filename = f"{output_dir}/Section_{section_num}_{section_title.replace(' ', '_')}.md"
                    
                    # Skip if already exists
                    if os.path.exists(filename):
                        print(f"⏭️  Skipping Section {section_num} (already exists)")
                        sections_generated += 1
                        continue
                    
                    # Submit for parallel processing
                    future = executor.submit(
                        self._generate_section_wrapper,
                        generator,
                        section_info,
                        idx,
                        len(sections),
                        output_dir
                    )
                    futures[future] = section_num
                
                # Wait for completion
                for future in as_completed(futures):
                    section_num = futures[future]
                    try:
                        result = future.result()
                        if result['success']:
                            sections_generated += 1
                            print(f"✅ Section {section_num} complete")
                        else:
                            section_errors.append(f"Section {section_num}: {result['error']}")
                            print(f"❌ Section {section_num} failed: {result['error']}")
                    except Exception as e:
                        section_errors.append(f"Section {section_num}: {str(e)}")
                        print(f"❌ Section {section_num} exception: {e}")
            
            return {
                'status': 'success' if not section_errors else 'partial',
                'sections_generated': sections_generated,
                'total_sections': len(sections),
                'errors': section_errors,
                'output_dir': output_dir
            }
        
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'sections_generated': 0
            }
    
    def _generate_section_wrapper(self, generator, section_info, idx, total, output_dir):
        """Wrapper for section generation with error handling."""
        try:
            # Temporarily change output directory
            original_output = "output"
            
            # Generate section (this will create the file)
            generate_section(generator, section_info, idx, total)
            
            # Move file to correct output directory
            section_num = section_info['section_number']
            section_title = section_info['section_title']
            original_file = f"output/Section_{section_num}_{section_title.replace(' ', '_')}.md"
            new_file = f"{output_dir}/Section_{section_num}_{section_title.replace(' ', '_')}.md"
            
            if os.path.exists(original_file):
                os.rename(original_file, new_file)
            
            return {'success': True}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def process_batch(self, outline_files: List[str], config: Config) -> Dict:
        """
        Process multiple outline files in parallel.
        
        Args:
            outline_files: List of outline file paths
            config: Config object
        
        Returns:
            Summary of batch processing
        """
        print(f"\n{'='*70}")
        print(f"🚀 BATCH PROCESSING - {len(outline_files)} OUTLINES")
        print(f"{'='*70}\n")
        
        start_time = time.time()
        
        # Process each outline in parallel
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self.process_single_outline, outline_file, config): outline_file
                for outline_file in outline_files
            }
            
            results = {}
            for future in as_completed(futures):
                outline_file = futures[future]
                try:
                    result = future.result()
                    results[outline_file] = result
                except Exception as e:
                    results[outline_file] = {
                        'status': 'error',
                        'error': str(e),
                        'sections_generated': 0
                    }
        
        elapsed_time = time.time() - start_time
        
        # Summary
        total_sections = sum(r.get('sections_generated', 0) for r in results.values())
        total_errors = sum(len(r.get('errors', [])) for r in results.values())
        
        summary = {
            'total_outlines': len(outline_files),
            'total_sections': total_sections,
            'total_errors': total_errors,
            'elapsed_time': elapsed_time,
            'results': results
        }
        
        return summary

def batch_generate():
    """Main function for batch generation."""
    print("\n" + "="*70)
    print("🚀 BATCH TEXTBOOK GENERATOR")
    print("="*70)
    
    # Find outline files
    processor = BatchProcessor(max_workers=3)
    outline_files = processor.find_outline_files()
    
    if not outline_files:
        print("\n❌ No outline files found!")
        print("\nLooking for files matching:")
        print("  - syllabus*.md")
        print("  - outline*.md")
        print("  - chapter*.md")
        print("  - *_outline.md")
        return
    
    print(f"\n📚 Found {len(outline_files)} outline files:")
    for i, file in enumerate(outline_files, 1):
        print(f"  [{i}] {file}")
    
    print(f"\n⚡ Processing with {processor.max_workers} parallel workers")
    print(f"   Estimated speed: {processor.max_workers}x faster than sequential\n")
    
    confirm = input("Start batch generation? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Cancelled")
        return
    
    # Process batch
    config = Config()
    summary = processor.process_batch(outline_files, config)
    
    # Print summary
    print(f"\n{'='*70}")
    print("BATCH GENERATION COMPLETE")
    print(f"{'='*70}")
    print(f"✅ Outlines processed: {summary['total_outlines']}")
    print(f"✅ Sections generated: {summary['total_sections']}")
    print(f"❌ Errors: {summary['total_errors']}")
    print(f"⏱️  Time: {summary['elapsed_time']/60:.1f} minutes")
    print(f"\nResults:")
    
    for outline_file, result in summary['results'].items():
        status_icon = "✅" if result['status'] == 'success' else "⚠️" if result['status'] == 'partial' else "❌"
        print(f"  {status_icon} {outline_file}: {result.get('sections_generated', 0)} sections")
        if result.get('errors'):
            for error in result['errors'][:2]:  # Show first 2 errors
                print(f"      - {error}")

if __name__ == "__main__":
    batch_generate()
