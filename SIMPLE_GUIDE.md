# Quick Guide: Generate Exactly Like Your Master Command Example

## The Confusion Explained

You showed me a Master Command with **16 subsections** (1.0 Introduction, 2.0 Types, 3.0 Modes, etc.).

The current system does **double expansion**:
- Takes your section → breaks into 15 topics → breaks each into 4 subsections = 60 parts

**You want single expansion**:
- Takes your section → breaks into 16 subsections → writes each one

## Solution: Use the Correct Script

Run this command:
```bash
python3 -m src.interactive_main
```

Then:
1. Choose a section number (e.g., `[1]` for "Types of Research Designs")
2. It will generate using the Master Command template
3. You'll get ~16 subsections per section (not 60)
4. Each subsection will be 2,000-4,000 words
5. Total: ~40,000 words per section

## What Happens

For "1. Surveys and Questionnaires":
```
1.0 Introduction to Surveys and Questionnaires
2.0 Types of Surveys  
3.0 Modes of Survey Data Collection
4.0 Designing a High-Quality Questionnaire
5.0 Writing Good Survey Questions
... (continues to 16.0)
```

Each of these gets written as full content (2,000-4,000 words each).

## No Progress Bar, But You Can Watch

- Open the file in `output/Section_1_Surveys_and_Questionnaires.md`
- Watch it grow in real-time as content is written
- Takes ~20-30 minutes per section

## Your 10 Sections

You have 10 sections, so:
- 10 sections × 16 subsections = 160 total subsections
- 10 sections × 40,000 words = 400,000 total words
- 10 sections × 25 minutes = ~4 hours total

This matches your Master Command example exactly!
