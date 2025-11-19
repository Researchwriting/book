# Parallel Generation - Speed Boost Guide

## ✅ What It Does

Generate **2 sections simultaneously** instead of one at a time.

**Speed improvement**: 2x faster (6 hours → 3 hours for 11 sections)

---

## How to Use

### Option 1: From Menu

```bash
python3 -m src.interactive_main
```

Choose `[p]` for parallel generation:

```
📋 Options:
  [1-11]  Generate a specific section
  [a]     Generate ALL sections (sequential)
  [p]     Generate ALL sections (PARALLEL - 2x faster)  ← NEW!

Your choice: p
```

---

### What Happens

```
🚀 PARALLEL GENERATION MODE
   This will generate 2 sections at a time (2x faster)
   Estimated time: ~110 minutes

Continue? (y/n): y

🔄 Starting parallel generation of 11 sections...

🔄 [Worker 1] Starting Section 1
🔄 [Worker 2] Starting Section 2

✅ [Worker 1] Completed Section 1
🔄 [Worker 1] Starting Section 3

✅ [Worker 2] Completed Section 2
🔄 [Worker 2] Starting Section 4

...

======================================================================
PARALLEL GENERATION COMPLETE
======================================================================
✅ Successful: 11
❌ Errors: 0
```

---

## How It Works

### Threading Model

- **2 worker threads** run simultaneously
- Each worker generates one section at a time
- When a worker finishes, it picks up the next pending section
- All workers share the same API key (DeepSeek allows this)

### Thread Safety

- ✅ File writing is isolated (each section = separate file)
- ✅ Cost tracking uses thread locks
- ✅ Resume manager uses thread locks
- ✅ Quality control is per-section

---

## Performance

### Sequential (Option [a])
```
Section 1: 20 min
Section 2: 20 min
Section 3: 20 min
...
Total: 11 × 20 = 220 minutes (~3.7 hours)
```

### Parallel (Option [p])
```
Worker 1: Section 1 (20 min) → Section 3 (20 min) → Section 5...
Worker 2: Section 2 (20 min) → Section 4 (20 min) → Section 6...

Total: 11 ÷ 2 × 20 = 110 minutes (~1.8 hours)
```

**Speed boost**: 2x faster!

---

## Safety Features

### Error Handling

If one section fails, others continue:

```
✅ [Worker 1] Completed Section 1
❌ [Worker 2] Error in Section 2: Network timeout
🔄 [Worker 2] Starting Section 3
```

### Resume Support

Parallel generation works with resume:
- Skips already-completed sections
- Only generates pending sections
- Each worker can resume its section if interrupted

### Cost Tracking

All workers update the same cost tracker:
```
💰 Cost so far: $0.0456 (24,500 tokens)
```

---

## Limitations

### 1. **API Rate Limits**
DeepSeek allows multiple concurrent requests, but if you hit rate limits:
- Reduce `max_workers` to 1 (sequential)
- Or add delays between requests

### 2. **Memory Usage**
- 2 workers = 2× memory usage (~60 MB instead of 30 MB)
- Still very light!

### 3. **Output Order**
Sections may complete out of order:
```
✅ Section 2 complete
✅ Section 1 complete
✅ Section 4 complete
✅ Section 3 complete
```

This is normal and doesn't affect the final output.

---

## Configuration

### Change Number of Workers

Edit `src/interactive_main.py`:

```python
# 2 workers (default)
parallel_gen = ParallelGenerator(max_workers=2)

# 3 workers (3x faster, but higher API load)
parallel_gen = ParallelGenerator(max_workers=3)

# 1 worker (same as sequential)
parallel_gen = ParallelGenerator(max_workers=1)
```

---

## When to Use

### Use Parallel ([p]) When:
- ✅ Generating many sections (5+)
- ✅ You want faster results
- ✅ Your internet is stable
- ✅ You're not hitting API rate limits

### Use Sequential ([a]) When:
- ✅ Generating 1-2 sections
- ✅ You want to monitor each section closely
- ✅ You're experiencing API errors
- ✅ You want to minimize API load

---

## Example Session

```bash
# Start generator
python3 -m src.interactive_main

# Choose parallel mode
Your choice: p

# Confirm
Continue? (y/n): y

# Wait ~1.8 hours for 11 sections
# (instead of ~3.7 hours sequential)

# All done!
✅ Successful: 11
❌ Errors: 0
```

---

## Summary

Parallel generation gives you a **2x speed boost** with no quality loss. Perfect for generating large textbooks quickly!
