# Semantic Scholar API Usage Analysis

## Summary

✅ **Chapters that USE Semantic Scholar API** (via `writer.py`):
- Chapter 1: Introduction
- Chapter 2: Literature Review  
- Chapter 3: Methodology
- Chapter 4: Data Presentation

❌ **Chapters that DO NOT use Semantic Scholar API**:
- Chapter 5: Results and Discussion
- Chapter 6: Summary, Conclusion and Recommendation

## Detailed Breakdown

### Chapters 1-4: Using `writer.write_section()`

**File**: `thesis_main.py` lines 104-177

**Flow**:
```python
for chapter in [CHAPTER ONE, TWO, THREE, FOUR]:
    for section in chapter.sections:
        content = writer.write_section(chapter_title, section, topic, case_study)
        # ↑ This calls Semantic Scholar API
```

**What happens in `writer.write_section()`**:
1. Calls `researcher.search_papers(query)` → **Semantic Scholar API**
2. Calls `researcher.search_web(query)` → Tavily API
3. Creates rich citation guide with abstracts
4. Passes to LLM with strict citation rules
5. LLM writes content with in-text citations
6. References saved to `reference_manager`

### Chapter 5: Using `Chapter5DiscussionGenerator`

**File**: `chapter5_generator.py`

**Flow**:
```python
ch5_generator.generate_chapter5(objectives, topic, case_study)
```

**What it does**:
- Retrieves Chapter 2 content (which already has citations)
- Retrieves Chapter 4 findings
- Synthesizes them
- **Does NOT call Semantic Scholar API directly**
- References existing citations from Chapter 2

**Problem**: Chapter 5 relies on Chapter 2 citations but doesn't fetch new papers

### Chapter 6: Using `Chapter6Generator`

**File**: `chapter6_generator.py`

**Flow**:
```python
ch6_generator.generate_chapter6(objectives, topic, case_study)
```

**What it does**:
- Summarizes all previous chapters
- **Does NOT call Semantic Scholar API**
- No new citations needed (just summarizing)

## Issues Identified

### ❌ Issue 1: Chapter 5 Doesn't Fetch New Papers
Chapter 5 should potentially fetch additional papers for discussion, but currently only references Chapter 2 citations.

**Current behavior**:
- Chapter 5 only uses citations that were already in Chapter 2
- No new literature is consulted for discussion

**Should it fetch new papers?**
- Debatable - typically Chapter 5 discusses findings in relation to Chapter 2 literature
- But it could benefit from additional recent studies

### ✅ Issue 2: Chapter 6 Correctly Doesn't Need Citations
Chapter 6 is a summary/conclusion chapter, so it doesn't need to fetch new papers.

## Recommendation

### Option 1: Keep as is (Recommended)
- Chapters 1-4 fetch papers ✅
- Chapter 5 uses Chapter 2 citations ✅
- Chapter 6 summarizes without new citations ✅

This is academically sound because:
- Literature review (Ch 2) establishes the theoretical foundation
- Discussion (Ch 5) relates findings back to that foundation
- Conclusion (Ch 6) synthesizes everything

### Option 2: Add Semantic Scholar to Chapter 5
If you want Chapter 5 to fetch additional papers for richer discussion:

```python
# In chapter5_generator.py, add:
from .researcher import Researcher

def _generate_objective_discussion(...):
    # Fetch additional papers for this objective
    researcher = Researcher(reference_manager)
    papers = researcher.search_papers(f"{topic} {objective_text}")
    # Include in discussion prompt
```

## Current Implementation Status

✅ **Semantic Scholar API is properly integrated** in:
- `researcher.py` - API calls with caching
- `writer.py` - Rich citation guide with abstracts
- `reference_manager.py` - Tracks all citations
- `thesis_main.py` - Generates bibliography after Chapter 6

✅ **All prompts updated** to:
- Forbid hallucinated citations
- Forbid reference sections at end
- Use only provided citations

✅ **Logging added** to track API calls:
- "🔍 Searching Semantic Scholar API for: ..."
- "📄 Found X papers from Semantic Scholar"
