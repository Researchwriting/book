"""
Verification Script - Test Full Parallel Flow with Notifications
"""
import os
import sys
import shutil
import unittest
from unittest.mock import MagicMock, patch

# Add current directory to path
sys.path.append(os.getcwd())

# from src.generator import Generator # Not needed
from src.config import Config
import src.docx_generator
import src.auto_notifier

class MockGenerator:
    def generate(self, prompt, max_tokens=None):
        return "This is dummy generated content for testing purposes."

def verify_flow():
    print("=" * 70)
    print("🧪 VERIFYING FULL PARALLEL FLOW")
    print("=" * 70)
    
    # Setup mocks
    print("\n1. Setting up mocks...")
    
    # Mock generator
    mock_gen = MockGenerator()
    
    # Mock inputs for generate_chapter
    # We need to mock input() calls inside generate_chapter
    # 1. Outline choice -> "2" (Paste outline)
    # 2. Paste outline -> "1. Test Section One\n2. Test Section Two"
    # 3. Confirm generation -> "y"
    
    input_side_effects = [
        "2",  # Paste outline
        "1. Test Section One",
        "2. Test Section Two",
        EOFError, # End of input
        "y"   # Start generation
    ]
    
    # Patching
    with patch('builtins.input', side_effect=input_side_effects) as mock_input, \
         patch('src.auto_notifier.load_notification_config') as mock_load_config, \
         patch('src.auto_notifier.AutoNotifier') as MockNotifier, \
         patch('src.docx_generator.auto_convert_to_docx') as mock_docx:
        
        # Configure mocks
        mock_load_config.return_value = {
            'email_enabled': True,
            'email_to': 'test@example.com',
            'email_from': 'sender@example.com',
            'email_password': 'pass'
        }
        
        mock_notifier_instance = MockNotifier.return_value
        
        # Import generate_chapter
        from generate import generate_chapter
        
        print("2. Running generate_chapter...")
        try:
            # Run generation
            topic = "Test Chapter Flow"
            generate_chapter(mock_gen, topic, 10000, "Test Context", "output/test.md")
            
            print("\n3. Verifying results...")
            
            # Check file structure
            chapter_dir = "output/Test_Chapter_Flow"
            if os.path.exists(chapter_dir):
                print(f"   ✅ Chapter directory created: {chapter_dir}")
            else:
                print(f"   ❌ Chapter directory missing: {chapter_dir}")
            
            sections_dir = f"{chapter_dir}/sections"
            if os.path.exists(sections_dir):
                print(f"   ✅ Sections directory created: {sections_dir}")
                files = os.listdir(sections_dir)
                print(f"   📂 Files found: {files}")
                
                md_files = [f for f in files if f.endswith('.md')]
                if len(md_files) == 2:
                    print(f"   ✅ Correct number of MD files (2)")
                else:
                    print(f"   ❌ Wrong number of MD files: {len(md_files)}")
            else:
                print(f"   ❌ Sections directory missing")
            
            # Check DOCX calls
            # We expect 2 calls for sections + 1 call for combined
            print(f"   📊 DOCX conversion calls: {mock_docx.call_count}")
            if mock_docx.call_count >= 2:
                print("   ✅ DOCX conversion triggered")
            else:
                print("   ❌ DOCX conversion NOT triggered enough times")
            
            # Check Email calls
            print(f"   📧 Email notification calls: {mock_notifier_instance.notify_section_complete.call_count}")
            if mock_notifier_instance.notify_section_complete.call_count == 2:
                print("   ✅ Email notifications triggered for both sections")
                
                # Verify arguments
                args = mock_notifier_instance.notify_section_complete.call_args_list
                print("   🔍 Email call arguments:")
                for i, call in enumerate(args):
                    print(f"      Call {i+1}: {call}")
            else:
                print("   ❌ Email notifications NOT triggered correctly")
            
        except Exception as e:
            print(f"\n❌ Error during verification: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Cleanup
            if os.path.exists("output/Test_Chapter_Flow"):
                shutil.rmtree("output/Test_Chapter_Flow")
                print("\n🧹 Cleaned up test output")

if __name__ == "__main__":
    verify_flow()
