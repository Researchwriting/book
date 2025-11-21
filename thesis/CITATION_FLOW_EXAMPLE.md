# How Citation Flow Works - Example

## Step 1: Semantic Scholar API Call

When generating a section like "2.3 Impact of Climate Change", the system:

```python
query = "Climate Change Impact South Sudan"
papers = researcher.search_papers(query)  # Calls Semantic Scholar API
```

## Step 2: What Semantic Scholar Returns

```json
[
  {
    "title": "Climate Change Adaptation in East Africa",
    "authors": [{"name": "Smith, John"}, {"name": "Doe, Jane"}],
    "year": 2023,
    "abstract": "This study examines climate change adaptation strategies in East African countries, focusing on agricultural resilience and water management. The research found that community-based approaches were 45% more effective than top-down interventions...",
    "venue": "Journal of Climate Research",
    "doi": "10.1234/jcr.2023.001"
  },
  {
    "title": "Economic Impacts of Drought in Sub-Saharan Africa",
    "authors": [{"name": "Johnson, Mary"}],
    "year": 2022,
    "abstract": "Analysis of economic losses due to prolonged drought periods across Sub-Saharan Africa. GDP reductions of 2-5% were observed in affected regions...",
    "venue": "African Economic Review"
  }
]
```

## Step 3: What the LLM Receives (NEW - ENHANCED)

```
CITATION GUIDE (Use ONLY these sources for in-text citations):
=== ACADEMIC PAPERS FROM SEMANTIC SCHOLAR ===

1. [Smith, 2023] "Climate Change Adaptation in East Africa"
   Authors: Smith, John, Doe, Jane
   Published in: Journal of Climate Research
   Abstract: This study examines climate change adaptation strategies in East African countries, focusing on agricultural resilience and water management. The research found that community-based approaches were 45% more effective than top-down interventions...
   
   HOW TO CITE: Use (Smith, 2023) or Smith (2023) in your text.
   WHEN TO USE: Cite this when discussing topics related to the abstract above.

2. [Johnson, 2022] "Economic Impacts of Drought in Sub-Saharan Africa"
   Authors: Johnson, Mary
   Published in: African Economic Review
   Abstract: Analysis of economic losses due to prolonged drought periods across Sub-Saharan Africa. GDP reductions of 2-5% were observed in affected regions...
   
   HOW TO CITE: Use (Johnson, 2022) or Johnson (2022) in your text.
   WHEN TO USE: Cite this when discussing topics related to the abstract above.
```

## Step 4: How the LLM Uses This

The LLM can now write **informed sentences** based on the abstracts:

### Example Output:

```
Climate change poses significant challenges to agricultural productivity in East Africa. 
Research has demonstrated that community-based adaptation strategies are substantially 
more effective than centralized interventions, with effectiveness rates improving by 
approximately 45% (Smith, 2023). The economic consequences of these climate impacts 
are severe, with prolonged drought periods resulting in GDP reductions ranging from 
2% to 5% across affected Sub-Saharan regions (Johnson, 2022).
```

## Step 5: Bibliography Generation

Later, after Chapter 6, the system generates:

```
# BIBLIOGRAPHY

Smith, J. and Doe, J. (2023) 'Climate Change Adaptation in East Africa', 
Journal of Climate Research. DOI: 10.1234/jcr.2023.001
  - Used in: CHAPTER TWO

Johnson, M. (2022) 'Economic Impacts of Drought in Sub-Saharan Africa', 
African Economic Review.
  - Used in: CHAPTER TWO
```

## Key Points

✅ **LLM sees the abstract** - Can write informed sentences
✅ **LLM knows the author and year** - Can cite correctly
✅ **LLM knows when to use each source** - Based on abstract content
✅ **No hallucination** - Can only cite what's in the guide
✅ **Bibliography is automatic** - Generated from the reference manager
