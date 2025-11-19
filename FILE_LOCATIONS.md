# File Locations and Memory Management

## Where Files Are Saved

### Output Directory
**Location**: `/home/gemtech/Desktop/map/output/`

### File Structure
```
output/
├── Section_1_Digital_and_Online_Research_Methods.md
├── Section_2_Use_of_Artificial_Intelligence_and_Machine_Learning.md
├── Section_3_Open_Science_and_Data_Sharing.md
├── ... (10 sections total)
└── Complete_Textbook.md (combined file)
```

### Current Status
- **Section 1**: Currently being written (in progress)
- **Sections 2-10**: Not started yet
- **Complete_Textbook.md**: Will be created after all sections finish

## Memory Management

### Original Design (RAM-Heavy)
```python
# BAD: Holds entire section in memory
content = ""
content += intro  # ~800 words
for topic in topics:
    for subsection in subsections:
        content += subsection_content  # ~1000 words each
# Total: ~40,000 words = ~200KB in RAM
# Then writes once at the end
```

### Optimized Design (Disk-Based)
```python
# GOOD: Writes incrementally
with open(filename, 'w') as f:
    f.write(intro)
    f.flush()  # Write to disk immediately
    for topic in topics:
        for subsection in subsections:
            f.write(subsection_content)
            f.flush()  # Write after each subsection
```

### Benefits
1. **Lower RAM usage**: Only holds ~1-2KB at a time (current subsection)
2. **Real-time progress**: File updates as content is generated
3. **Crash recovery**: Partial progress is saved
4. **Better performance**: No large string concatenations

### Current Memory Usage
```
python3 process: 30 MB RAM (very light)
```

### Why PC Performance Lowered
**Not RAM** - The process uses minimal memory.

**Likely causes**:
1. **Network I/O**: Waiting for DeepSeek API responses
2. **CPU idle time**: Process spends most time waiting for API
3. **Background processes**: Other system tasks

### How to Monitor
```bash
# Check memory usage
ps aux | grep textbook_main

# Check output file size (while running)
watch -n 5 'ls -lh output/'

# Check word count (while running)
watch -n 10 'wc -w output/Section_1_*.md'
```

## Viewing Progress

### Option 1: Tail the output file
```bash
tail -f output/Section_1_Digital_and_Online_Research_Methods.md
```

### Option 2: Check word count
```bash
wc -w output/Section_1_*.md
```

### Option 3: View in real-time
```bash
# Open the file in a text editor that auto-refreshes
# The file updates every ~30 seconds (after each subsection)
```

## File Format

All files are saved as **Markdown (.md)** format.

### To Convert to DOCX
```bash
# Install pandoc
sudo apt install pandoc

# Convert single section
pandoc output/Section_1_Digital_and_Online_Research_Methods.md -o Section_1.docx

# Convert complete textbook
pandoc output/Complete_Textbook.md -o Complete_Textbook.docx
```

### To Convert to PDF
```bash
# Install pandoc and LaTeX
sudo apt install pandoc texlive-latex-base

# Convert
pandoc output/Complete_Textbook.md -o Complete_Textbook.pdf
```
