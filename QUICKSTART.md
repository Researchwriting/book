# Quick Start Guide

## Run the Textbook Generator

### Option 1: Interactive Mode (RECOMMENDED) 🎮
**Choose which sections to generate, pause/resume, see progress**

```bash
cd /home/gemtech/Desktop/map
python3 -m src.interactive_main
```

### Option 2: Multi-Step Mode (Automatic)
**Generates all sections automatically**

```bash
cd /home/gemtech/Desktop/map
python3 -m src.multistep_main
```

### Option 3: Standard Mode
```bash
cd /home/gemtech/Desktop/map
python3 -m src.textbook_main
```

## What It Does

1. Reads `syllabus.md` (your chapter outline)
2. For each section:
   - Generates 12 topics
   - Expands each topic into 4 subsections
   - Writes ~1000 words per subsection
   - Total: ~40,000 words per section
3. Saves to `output/Section_X_Title.md`
4. Combines all sections into `output/Complete_Textbook.md`

## Monitor Progress

```bash
# Check if running
ps aux | grep textbook_main

# Watch output folder
watch -n 5 'ls -lh output/'

# Count words
wc -w output/*.md
```

## Stop the Generator

```bash
# Press Ctrl+C in the terminal
# OR
pkill -f textbook_main
```

## Customize

### Edit the Syllabus
```bash
nano syllabus.md
```

### Change Settings
Edit `src/config.py`:
- `API_KEY`: Your DeepSeek API key
- `MODEL_NAME`: Model to use (default: `deepseek-chat`)

### Adjust Word Count
Edit `src/textbook_planner.py`:
- `num_topics=12`: More topics = longer sections
- `num_subsections=4`: More subsections = more detail

## Output Files

All files saved to: `/home/gemtech/Desktop/map/output/`

- Individual sections: `Section_1_Title.md`, `Section_2_Title.md`, etc.
- Complete book: `Complete_Textbook.md`

## Convert to DOCX/PDF

```bash
# Install pandoc
sudo apt install pandoc

# Convert to Word
pandoc output/Complete_Textbook.md -o Complete_Textbook.docx

# Convert to PDF (requires LaTeX)
sudo apt install texlive-latex-base
pandoc output/Complete_Textbook.md -o Complete_Textbook.pdf
```

## Estimated Time

- **1 section**: ~20-30 minutes
- **10 sections**: ~3-4 hours
- **Total output**: ~400,000 words

## Cost (DeepSeek)

- Approximately **$0.20 - $0.50** for 400,000 words
- Much cheaper than GPT-4 (~$15-20) or Gemini (~$2-5)

## Troubleshooting

### API Errors
Check your API key in `src/config.py`

### Out of Memory
The system uses only ~30 MB RAM. If you see issues, it's likely network/API related, not memory.

### Slow Performance
This is normal - waiting for API responses. Each subsection takes ~30-60 seconds.

### Empty Output Folder
Files are written incrementally but only appear when a section completes.

## Test with One Section

To test quickly, edit `syllabus.md` to have only 1 section:

```markdown
# Chapter 10: Test
## 1. Digital and Online Research Methods
```

Then run:
```bash
python3 -m src.textbook_main
```
