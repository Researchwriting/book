# Resume from Interruption - Feature Guide

## ✅ How It Works

The system now **automatically saves progress** after each subsection is written. If generation is interrupted (crash, Ctrl+C, network error), you can **resume exactly where you left off**.

---

## Automatic Saving

### What Gets Saved
- ✅ Completed subsections
- ✅ Completed topics  
- ✅ Section status (in progress / completed)
- ✅ Progress tracking

### Save Location
```
output/.generation_state.json
```

This file is automatically created and updated after each subsection.

---

## How to Resume

### Scenario 1: Generation Crashes

```
✏️  Writing: Research Design Principles... ✅
✏️  Writing: Ethical Considerations... ❌ Error: Network timeout
💾 Progress saved. You can resume later.
```

**What to do:**
1. Run the generator again: `python3 -m src.interactive_main`
2. Choose the same section number
3. You'll see:

```
⚠️  Found partial progress for this section!
   Completed: 15 subsections

[r] Resume from where you left off
[s] Start fresh (delete progress)
[c] Cancel

Your choice: r
```

4. Press `r` to resume
5. Generation continues from subsection 16

---

### Scenario 2: You Stop Manually (Ctrl+C)

```
✏️  Writing: Data Collection Methods... ✅
✏️  Writing: Sampling Strategies... ^C

👋 Interrupted by user. Goodbye!
```

**What to do:**
1. Run again: `python3 -m src.interactive_main`
2. Choose the same section
3. Press `r` to resume from where you stopped

---

### Scenario 3: You Want to Start Over

```
⚠️  Found partial progress for this section!
   Completed: 15 subsections

[r] Resume from where you left off
[s] Start fresh (delete progress)
[c] Cancel

Your choice: s
```

Press `s` to delete progress and start from scratch.

---

## What Gets Skipped

When resuming, the system **skips already-completed subsections**:

```
📚 Topic 3/12: Research Design Types
   ⏭️  Skipping: Experimental Designs (already done)
   ⏭️  Skipping: Correlational Designs (already done)
   ✏️  Writing: Case Study Designs... ✅
```

This saves time and avoids duplicate work.

---

## State File Format

```json
{
  "1": {
    "section_title": "Types of Research Designs",
    "status": "in_progress",
    "total_topics": 12,
    "completed_topics": [1, 2],
    "completed_subsections": [
      "1.1", "1.2", "1.3", "1.4",
      "2.1", "2.2", "2.3", "2.4",
      "3.1", "3.2"
    ]
  }
}
```

---

## Error Handling

The system wraps subsection generation in try/catch:

```python
try:
    # Generate subsection
    subsection_content = write_subsection(...)
    
    # Save to file
    f.write(subsection_content)
    
    # Mark as completed
    resume_manager.complete_subsection(...)

except Exception as e:
    print("❌ Error: {e}")
    print("💾 Progress saved. You can resume later.")
    raise
```

Even if generation fails, **all previous subsections are saved**.

---

## Benefits

✅ **Never lose work** - Progress saved after each subsection
✅ **Resume anytime** - Pick up exactly where you left off  
✅ **Flexible** - Choose to resume or restart
✅ **Automatic** - No manual intervention needed
✅ **Safe** - Error handling ensures state is always saved

---

## Example Session

```bash
# Start generation
python3 -m src.interactive_main
Your choice: 1

# ... generates 15 subsections ...
# ... network error occurs ...

💾 Progress saved. You can resume later.

# Restart
python3 -m src.interactive_main
Your choice: 1

⚠️  Found partial progress!
   Completed: 15 subsections

[r] Resume
Your choice: r

✅ Resuming from last checkpoint...
⏭️  Skipping subsections 1-15 (already done)
✏️  Writing subsection 16... ✅
```

---

## Summary

The resume feature makes long-running generation **safe and reliable**. You can stop anytime and continue later without losing progress.
