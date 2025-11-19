# Batch Processing Guide - FAST & INTELLIGENT

## ✅ What It Does

Generate **multiple textbooks from multiple outline files** simultaneously.

**Speed**: 3x faster than processing one at a time
**Intelligence**: Auto-detects outline files, skips completed sections, handles errors gracefully

---

## How to Use

### Step 1: Prepare Your Outline Files

Create multiple outline files with these naming patterns:
```
syllabus_psychology.md
syllabus_economics.md
outline_sociology.md
chapter_biology.md
research_methods_outline.md
```

### Step 2: Run Batch Processor

```bash
cd /home/gemtech/Desktop/map
python3 -m src.batch_processor
```

### What Happens

```
🚀 BATCH TEXTBOOK GENERATOR
======================================================================

📚 Found 3 outline files:
  [1] syllabus_psychology.md
  [2] syllabus_economics.md
  [3] outline_sociology.md

⚡ Processing with 3 parallel workers
   Estimated speed: 3x faster than sequential

Start batch generation? (y/n): y

======================================================================
📚 Processing: syllabus_psychology.md
======================================================================
📁 Output directory: output/syllabus_psychology
📊 Found 11 sections to generate

🔄 [Worker 1] Starting Section 1
🔄 [Worker 2] Starting Section 2
...

======================================================================
BATCH GENERATION COMPLETE
======================================================================
✅ Outlines processed: 3
✅ Sections generated: 33
❌ Errors: 0
⏱️  Time: 65.3 minutes

Results:
  ✅ syllabus_psychology.md: 11 sections
  ✅ syllabus_economics.md: 11 sections
  ✅ syllabus_sociology.md: 11 sections
```

---

## Intelligence Features

### 1. **Auto-Detection**
Automatically finds outline files matching:
- `syllabus*.md`
- `outline*.md`
- `chapter*.md`
- `*_outline.md`

### 2. **Smart Skipping**
Skips already-generated sections:
```
⏭️  Skipping Section 1 (already exists)
⏭️  Skipping Section 2 (already exists)
🔄 Generating Section 3...
```

### 3. **Separate Output Directories**
Each outline gets its own directory:
```
output/
├── syllabus_psychology/
│   ├── Section_1_*.md
│   ├── Section_2_*.md
│   └── master_commands/
├── syllabus_economics/
│   ├── Section_1_*.md
│   └── master_commands/
└── outline_sociology/
    └── ...
```

### 4. **Error Resilience**
If one outline fails, others continue:
```
✅ syllabus_psychology.md: 11 sections
❌ syllabus_economics.md: Error: Invalid format
✅ outline_sociology.md: 11 sections
```

---

## Speed Comparison

### Sequential (One at a Time)
```
Outline 1: 3.5 hours
Outline 2: 3.5 hours
Outline 3: 3.5 hours
Total: 10.5 hours
```

### Batch Processing (3 Parallel Workers)
```
All 3 outlines: ~3.5 hours
Total: 3.5 hours
```

**Speed boost: 3x faster!**

---

## Configuration

### Change Number of Workers

Edit `src/batch_processor.py` line 16:

```python
# 3 workers (default - 3x faster)
processor = BatchProcessor(max_workers=3)

# 5 workers (5x faster, but higher API load)
processor = BatchProcessor(max_workers=5)

# 2 workers (2x faster, safer)
processor = BatchProcessor(max_workers=2)
```

---

## Use Cases

### 1. **Multiple Textbooks**
Generate psychology, economics, and sociology textbooks simultaneously

### 2. **Different Chapters**
Process Chapter 1, Chapter 2, Chapter 3 in parallel

### 3. **Different Contexts**
Generate same content for African, Asian, and Western contexts

### 4. **Batch Updates**
Regenerate multiple textbooks after updating prompts

---

## Example: Generate 5 Textbooks

```bash
# Create 5 outline files
syllabus_psychology.md
syllabus_economics.md
syllabus_sociology.md
syllabus_anthropology.md
syllabus_political_science.md

# Run batch processor
python3 -m src.batch_processor

# Result: 5 textbooks in ~3.5 hours
# (instead of 17.5 hours sequential)
```

---

## Summary

Batch processing is **FAST** (3x speed), **INTELLIGENT** (auto-detects, skips duplicates), and **EFFICIENT** (parallel workers, error handling).

Perfect for generating multiple textbooks quickly!
