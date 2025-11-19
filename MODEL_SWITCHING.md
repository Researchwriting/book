# Model Switching Guide - DeepSeek ⇄ Gemini

## Why DeepSeek and Gemini?

Both are **extremely cheap** compared to GPT-4 and Claude:

```
💰 Cost for 400,000 words:
  DeepSeek: $0.20-0.50  ✅ CHEAP
  Gemini:   $0.15-0.40  ✅ CHEAP
  GPT-4:    $15-20      ❌ EXPENSIVE
  Claude:   $12-18      ❌ EXPENSIVE
```

---

## How to Switch Models

### From Interactive Menu

```bash
python3 -m src.interactive_main
```

Press `[x]` to switch models:

```
🔄 Switch AI Model

Current model: deepseek (deepseek-chat)

Available models:
  [1] DeepSeek (cheapest, good quality)
  [2] Gemini (cheapest, fast)
  [3] Show cost comparison

Your choice: 2

✅ Switched to Gemini
   Model: gemini-1.5-flash
   Cost: ~$0.075 input / $0.30 output per 1M tokens
```

---

## Setting Up Gemini

### Option 1: Environment Variable (Recommended)

```bash
export GEMINI_API_KEY="your-api-key-here"
python3 -m src.interactive_main
```

### Option 2: Edit Config File

Edit `src/model_switcher.py` line 28:

```python
config.API_KEY = "your-gemini-api-key-here"
```

---

## When to Use Each Model

### Use DeepSeek When:
- ✅ You want the absolute cheapest option
- ✅ You need long context (DeepSeek handles 32k tokens)
- ✅ You're generating many sections

### Use Gemini When:
- ✅ You want slightly faster responses
- ✅ You prefer Google's infrastructure
- ✅ You already have a Gemini API key

---

## Cost Comparison

### Full Textbook (11 sections, 440,000 words)

| Model | Input Cost | Output Cost | Total |
|-------|-----------|-------------|-------|
| DeepSeek | $0.07 | $0.14 | **$0.21** |
| Gemini | $0.04 | $0.15 | **$0.19** |
| GPT-4 | $2.50 | $7.50 | **$10.00** |
| Claude | $1.50 | $7.50 | **$9.00** |

**DeepSeek and Gemini are 50x cheaper than GPT-4/Claude!**

---

## Current Model Display

The menu shows your current model:

```
======================================================================
🎓 INTERACTIVE TEXTBOOK GENERATOR
   Model: deepseek (deepseek-chat)
======================================================================
```

Or:

```
======================================================================
🎓 INTERACTIVE TEXTBOOK GENERATOR
   Model: gemini (gemini-1.5-flash)
======================================================================
```

---

## Summary

You can easily switch between **DeepSeek** and **Gemini** - both are extremely cheap and perfect for generating large textbooks!
