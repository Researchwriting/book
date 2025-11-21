#!/usr/bin/env python3
import os
import sys
import subprocess
import time

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def print_header():
    print("=" * 60)
    print("🚀 UNIVERSAL CONTENT GENERATOR SYSTEM")
    print("=" * 60)
    print()

def run_book_generator():
    print("\n📚 Launching Book Generator...")
    time.sleep(1)
    # Run the interactive main from the books directory
    # We use subprocess to ensure it runs in the correct directory context
    try:
        subprocess.run([sys.executable, "-m", "src.interactive_main"], cwd="books")
    except KeyboardInterrupt:
        pass

def run_thesis_generator():
    print("\n🎓 Launching Thesis Generator...")
    time.sleep(1)
    try:
        # Run as a module from the root
        subprocess.run([sys.executable, "-m", "thesis.src.thesis_main"])
    except KeyboardInterrupt:
        pass

def show_placeholder(name):
    print(f"\n🚧 {name} is under development.")
    print("   Coming soon in a future update!")
    input("\nPress Enter to return to menu...")

def main():
    while True:
        clear_screen()
        print_header()
        print("Select a tool to launch:")
        print()
        print("  [1] 📚 Book Generator (Textbooks, Non-fiction)")
        print("  [2] 🎓 Thesis Generator (Academic Papers)")
        print("  [3] 📊 Data Analysis Suite")
        print("  [4] 📝 Content Editor")
        print("  [5] 📖 Story/Novel Generator (Legacy)")
        print()
        print("  [q] Quit")
        print()
        
        choice = input("Your choice: ").strip().lower()
        
        if choice == '1':
            run_book_generator()
        elif choice == '2':
            run_thesis_generator()
        elif choice == '3':
            show_placeholder("Data Analysis Suite")
        elif choice == '4':
            show_placeholder("Content Editor")
        elif choice == '5':
            # Legacy support
            print("\n📖 Launching Story Generator...")
            try:
                subprocess.run([sys.executable, "-m", "src.main"], cwd="books")
            except KeyboardInterrupt:
                pass
        elif choice == 'q':
            print("\n👋 Goodbye!")
            sys.exit(0)
        else:
            input("\n❌ Invalid choice. Press Enter to try again...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
