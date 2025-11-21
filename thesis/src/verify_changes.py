import sys
import os

# Add src to path
sys.path.append('/home/gemtech/Desktop/map/thesis/src')

from researcher import Researcher
from writer import ThesisWriter
import chapter2_prompts
import chapter3_prompts

def test_researcher_no_mock_data():
    print("Testing Researcher for NO MOCK DATA...")
    r = Researcher()
    # Force invalid API key to trigger failure/fallback
    r.api_key = "INVALID_KEY_FOR_TESTING" 
    
    # This should return [] now, not mock data
    results = r.search_papers("test query")
    
    if results == []:
        print("✅ Researcher returned empty list on failure (Correct).")
    else:
        print(f"❌ Researcher returned data: {results} (Incorrect - likely mock data).")
        # Check if it looks like the old mock data
        if len(results) > 0 and results[0].get('venue') == "Journal of Advanced Studies":
             print("   -> CONFIRMED: This is the old mock data!")

def test_prompts_have_warnings():
    print("\nTesting Prompts for Strict Warnings...")
    
    # Check Writer default prompt
    w = ThesisWriter()
    default_prompt = w._get_default_prompt("Ch1", "Sec1", "Topic", "Case", "", "")
    if "DO NOT INVENT OR HALLUCINATE CITATIONS" in default_prompt:
        print("✅ Writer default prompt has warning.")
    else:
        print("❌ Writer default prompt MISSING warning.")

    # Check Chapter 2 Prompts
    p2_theory = chapter2_prompts.get_chapter2_theory_prompt("Title", "Topic", "Case", "")
    if "STRICT PROHIBITION" in p2_theory:
        print("✅ Chapter 2 Theory prompt has warning.")
    else:
        print("❌ Chapter 2 Theory prompt MISSING warning.")

    # Check Chapter 3 Prompts
    p3_intro = chapter3_prompts.get_chapter3_introduction_prompt("Title", "Topic", "Case", "", "")
    if "STRICT PROHIBITION" in p3_intro:
        print("✅ Chapter 3 Intro prompt has warning.")
    else:
        print("❌ Chapter 3 Intro prompt MISSING warning.")

if __name__ == "__main__":
    test_researcher_no_mock_data()
    test_prompts_have_warnings()
