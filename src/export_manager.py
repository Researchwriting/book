"""
Export Manager - Convert markdown to DOCX and PDF
"""
import os
import subprocess

def export_to_docx(md_file: str, output_file: str = None) -> bool:
    """
    Export markdown to DOCX using pandoc.
    
    Args:
        md_file: Path to markdown file
        output_file: Optional output path (default: same name with .docx)
    
    Returns:
        True if successful
    """
    if output_file is None:
        output_file = md_file.replace('.md', '.docx')
    
    try:
        # Check if pandoc is installed
        result = subprocess.run(['which', 'pandoc'], capture_output=True)
        if result.returncode != 0:
            print("❌ Pandoc not installed. Install with: sudo apt install pandoc")
            return False
        
        # Convert
        cmd = ['pandoc', md_file, '-o', output_file]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Exported to DOCX: {output_file}")
            return True
        else:
            print(f"❌ Export failed: {result.stderr}")
            return False
    
    except Exception as e:
        print(f"❌ Export error: {e}")
        return False

def export_to_pdf(md_file: str, output_file: str = None) -> bool:
    """
    Export markdown to PDF using pandoc.
    
    Args:
        md_file: Path to markdown file
        output_file: Optional output path (default: same name with .pdf)
    
    Returns:
        True if successful
    """
    if output_file is None:
        output_file = md_file.replace('.md', '.pdf')
    
    try:
        # Check if pandoc is installed
        result = subprocess.run(['which', 'pandoc'], capture_output=True)
        if result.returncode != 0:
            print("❌ Pandoc not installed. Install with: sudo apt install pandoc")
            return False
        
        # Convert
        cmd = ['pandoc', md_file, '-o', output_file, '--pdf-engine=xelatex']
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Exported to PDF: {output_file}")
            return True
        else:
            print(f"❌ Export failed: {result.stderr}")
            print("💡 Tip: Install LaTeX with: sudo apt install texlive-xetex")
            return False
    
    except Exception as e:
        print(f"❌ Export error: {e}")
        return False

def auto_export_all(output_dir: str = "output"):
    """
    Automatically export all markdown files to DOCX and PDF.
    """
    print("\n📦 Auto-exporting all sections...")
    
    md_files = []
    for file in os.listdir(output_dir):
        if file.endswith('.md') and file.startswith('Section_'):
            md_files.append(os.path.join(output_dir, file))
    
    # Also export complete textbook
    complete_file = os.path.join(output_dir, 'Complete_Textbook.md')
    if os.path.exists(complete_file):
        md_files.append(complete_file)
    
    success_count = 0
    for md_file in md_files:
        if export_to_docx(md_file):
            success_count += 1
    
    print(f"\n✅ Exported {success_count}/{len(md_files)} files to DOCX")
    
    # Try PDF (optional, may fail if LaTeX not installed)
    print("\n📄 Attempting PDF export...")
    if os.path.exists(complete_file):
        export_to_pdf(complete_file)
