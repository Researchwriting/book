"""
Interactive Outline Input - Let users paste their own chapter outline
"""
import os

def get_user_outline():
    """
    Prompt user to paste their chapter outline.
    Returns the outline as a string.
    """
    print("\n" + "=" * 70)
    print("📝 PASTE YOUR CHAPTER OUTLINE")
    print("=" * 70)
    print("\nFormat:")
    print("  # Chapter Title")
    print("  ## 1. Section One Title")
    print("  ## 2. Section Two Title")
    print("  ...")
    print("\nPaste your outline below, then press Ctrl+D (Linux/Mac) or Ctrl+Z (Windows) when done:")
    print("-" * 70)
    
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    
    outline = "\n".join(lines)
    return outline

def save_outline_to_file(outline: str, filename: str = "syllabus.md"):
    """
    Save the user's outline to a file.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(outline)
    print(f"\n✅ Outline saved to {filename}")

def interactive_outline_input():
    """
    Main function to get outline from user and save it.
    """
    print("\n" + "=" * 70)
    print("🎓 TEXTBOOK GENERATOR - Custom Outline Input")
    print("=" * 70)
    
    choice = input("\n[1] Paste a new outline\n[2] Use existing syllabus.md\n\nYour choice: ").strip()
    
    if choice == "1":
        outline = get_user_outline()
        
        if not outline.strip():
            print("\n❌ No outline provided. Exiting.")
            return False
        
        # Show preview
        print("\n" + "=" * 70)
        print("📋 OUTLINE PREVIEW")
        print("=" * 70)
        print(outline[:500] + ("..." if len(outline) > 500 else ""))
        
        confirm = input("\n\nSave this outline? (y/n): ").strip().lower()
        
        if confirm == 'y':
            save_outline_to_file(outline)
            return True
        else:
            print("\n❌ Cancelled.")
            return False
    
    elif choice == "2":
        if os.path.exists("syllabus.md"):
            print("\n✅ Using existing syllabus.md")
            return True
        else:
            print("\n❌ syllabus.md not found. Please paste a new outline.")
            return interactive_outline_input()
    
    else:
        print("\n❌ Invalid choice.")
        return False

if __name__ == "__main__":
    interactive_outline_input()
