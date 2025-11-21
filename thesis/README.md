# PhD Thesis Generator

An intelligent multi-agent system for generating complete PhD theses with real data analysis, peer review, and academic citations.

## Features

✅ **Complete Thesis Generation** (Chapters 1-6)  
✅ **Real Data Analysis** (pandas-based statistical analysis)  
✅ **Semantic Scholar Integration** (300+ academic citations)  
✅ **Peer Review System** (3-reviewer panel)  
✅ **Study Tool Design** (questionnaires/interview guides)  
✅ **CSV Dataset Generation** (realistic simulated data)  
✅ **Email Notifications** (per-chapter with reviews)  
✅ **DOCX Formatting** (academic thesis standards)  
✅ **UK English Compliance**  
✅ **State Management** (resume capability)  

## Quick Start

### 1. Install Dependencies

```bash
# Ubuntu/Debian
sudo apt install python3-pandas python3-openpyxl python3-requests

# Or via pip (in virtual environment)
pip install -r thesis/requirements.txt
```

### 2. Configure API Keys

Edit `thesis/src/config.py`:
```python
DEEPSEEK_API_KEY = "your-key-here"
SEMANTIC_SCHOLAR_API_KEY = "your-key-here"
TAVILY_API_KEY = "your-key-here"
```

### 3. Run Thesis Generator

```bash
cd /path/to/map
python test_thesis.py
```

Or via menu:
```bash
python main.py
# Select [2] for Thesis Generator
```

## System Architecture

```
Chapter 1 (Introduction)
    ↓
Chapter 2 (Literature Review) + Semantic Scholar API
    ↓
Chapter 3 (Methodology)
    ↓
Study Tool Design → CSV Data Generation
    ↓
Chapter 4 (Data Analysis) - Real pandas analysis
    ↓
Chapter 5 (Discussion)
    ↓
Chapter 6 (Conclusion)
    ↓
Bibliography + Appendices
```

## Output

- **Thesis**: `thesis/output/Thesis_[Topic].md` (Markdown)
- **Thesis**: `thesis/output/Thesis_[Topic].docx` (DOCX)
- **Reviews**: `thesis/reviews/Combined_Review_CHAPTER_*.md`
- **Data**: `thesis/data/Quantitative_Data.csv`
- **Bibliography**: `thesis/references/bibliography.md`
- **State**: `thesis_state.json` (for resume)

## VPS Deployment

Run on VPS with `screen` to keep running after disconnect:

```bash
# Upload to VPS
scp -r thesis user@vps:/home/user/

# SSH and run in screen
ssh user@vps
screen -S thesis
cd /home/user/thesis
python test_thesis.py

# Detach: Ctrl+A then D
# Reconnect: screen -r thesis
```

## Email Notifications

Configure in `thesis/src/config.py`:
```python
EMAIL_ENABLED = True
EMAIL_ADDRESS = "your-gmail@gmail.com"
EMAIL_PASSWORD = "your-app-password"
RECIPIENT_EMAIL = "recipient@email.com"
```

Receives email per chapter with:
- Chapter content (MD + DOCX)
- Consolidated review report

## Project Structure

```
thesis/
├── src/
│   ├── thesis_main.py          # Main orchestrator
│   ├── writer.py                # Content generation
│   ├── researcher.py            # Semantic Scholar API
│   ├── reviewer.py              # Peer review panel
│   ├── reference_manager.py     # Citations & bibliography
│   ├── state_manager.py         # State persistence
│   ├── instrument_designer.py   # Study tools
│   ├── email_notifier.py        # Email notifications
│   ├── docx_formatter.py        # DOCX conversion
│   ├── chapter5_generator.py    # Discussion chapter
│   ├── chapter6_generator.py    # Conclusion chapter
│   └── analysis/
│       ├── data_analysis_orchestrator.py
│       ├── quantitative_analyzer.py
│       └── qualitative_analyzer.py
├── requirements.txt
└── README.md
```

## Features in Detail

### Real Data Analysis
- Generates realistic CSV datasets based on study tools
- Performs actual statistical analysis with pandas
- Creates correlation matrices, descriptive statistics
- Extracts qualitative themes and quotes

### Semantic Scholar Integration
- Searches 300+ academic papers
- Includes abstracts in citation guide
- Prevents hallucinated citations
- Harvard-style bibliography

### Peer Review System
- 3 reviewers: Supportive Mentor, Harsh Critic, Methodologist
- Reviews every section
- Improves content based on feedback
- Saves review reports

### State Management
- Saves progress after each section
- Resume from interruption
- Cross-chapter memory (Ch6 remembers Ch1 objectives)

## Timing

**Full thesis generation**: 3-4 hours (sequential)

**Chapters**:
- Chapter 1: ~80 min (40 sections)
- Chapter 2: ~45 min (15 sections + Semantic Scholar)
- Chapter 3: ~20 min (10 sections)
- Chapter 4: ~10 min (data analysis)
- Chapter 5: ~16 min (8 sections)
- Chapter 6: ~12 min (6 sections)

## Roadmap

### Coming Soon
- [ ] Parallel multi-agent architecture (2-3x faster)
- [ ] Docker container support
- [ ] Section-level parallelism (10x faster)
- [ ] Web UI for progress monitoring
- [ ] Multiple LLM provider support

## Requirements

- Python 3.8+
- pandas
- openpyxl
- python-docx
- requests

## License

MIT

## Contributing

Pull requests welcome! Please ensure:
- Code follows existing style
- All tests pass
- Documentation updated

## Support

For issues, please open a GitHub issue with:
- Error message
- Steps to reproduce
- System information

## Credits

Built with:
- DeepSeek API (LLM)
- Semantic Scholar API (citations)
- Tavily API (web search)
- pandas (data analysis)
