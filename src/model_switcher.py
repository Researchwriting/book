"""
Model Switcher - Easy switching between DeepSeek and Gemini
"""
from src.config import Config, LLMProvider

def switch_model(provider: str) -> Config:
    """
    Switch between AI models.
    
    Args:
        provider: 'deepseek' or 'gemini'
    
    Returns:
        Updated Config object
    """
    config = Config()
    
    if provider.lower() == 'deepseek':
        config.PROVIDER = LLMProvider.DEEPSEEK
        config.API_KEY = "sk-e336533d15ce4e1b8815977915600e6b"
        config.MODEL_NAME = "deepseek-chat"
        print("✅ Switched to DeepSeek")
        print("   Model: deepseek-chat")
        print("   Cost: ~$0.14 input / $0.28 output per 1M tokens")
    
    elif provider.lower() == 'gemini':
        config.PROVIDER = LLMProvider.GEMINI
        # User should set their Gemini API key here
        config.API_KEY = os.getenv('GEMINI_API_KEY', 'YOUR_GEMINI_API_KEY_HERE')
        config.MODEL_NAME = "gemini-1.5-pro"
        print("✅ Switched to Gemini Pro")
        print("   Model: gemini-1.5-pro")
        print("   Cost: ~$1.25 input / $5.00 output per 1M tokens")
        print("   Speed: Balanced")
        
        if config.API_KEY == 'YOUR_GEMINI_API_KEY_HERE':
            print("\n⚠️  WARNING: Set your Gemini API key!")
            print("   Option 1: Set environment variable GEMINI_API_KEY")
            print("   Option 2: Edit src/model_switcher.py line 28")
    
    elif provider.lower() in ['gemini-flash', 'flash']:
        config.PROVIDER = LLMProvider.GEMINI_FLASH
        config.API_KEY = os.getenv('GEMINI_API_KEY', 'YOUR_GEMINI_API_KEY_HERE')
        config.MODEL_NAME = "gemini-1.5-flash"
        print("✅ Switched to Gemini Flash (ULTRA-FAST)")
        print("   Model: gemini-1.5-flash")
        print("   Cost: ~$0.075 input / $0.30 output per 1M tokens")
        print("   Speed: 10x faster than DeepSeek")
        print("   🚀 Production mode: 3-5 min per section")
        
        if config.API_KEY == 'YOUR_GEMINI_API_KEY_HERE':
            print("\n⚠️  WARNING: Set your Gemini API key!")
            print("   Option 1: Set environment variable GEMINI_API_KEY")
            print("   Option 2: Edit src/model_switcher.py line 28")
    
    else:
        print(f"❌ Unknown provider: {provider}")
        print("   Available: 'deepseek', 'gemini', 'gemini-flash'")
        return None
    
    return config

def get_current_model(config: Config) -> str:
    """Get current model name."""
    return f"{config.PROVIDER.value} ({config.MODEL_NAME})"

def compare_costs():
    """Show cost comparison."""
    print("\n💰 Cost Comparison (per 1M tokens):")
    print("\n┌─────────────┬──────────┬───────────┐")
    print("│ Provider    │ Input    │ Output    │")
    print("├─────────────┼──────────┼───────────┤")
    print("│ DeepSeek    │ $0.14    │ $0.28     │  ← CHEAPEST")
    print("│ Gemini      │ $0.075   │ $0.30     │  ← CHEAPEST")
    print("│ GPT-4       │ $5.00    │ $15.00    │  ← EXPENSIVE!")
    print("│ Claude      │ $3.00    │ $15.00    │  ← EXPENSIVE!")
    print("└─────────────┴──────────┴───────────┘")
    print("\nFor 400,000 words (~500k tokens):")
    print("  DeepSeek: ~$0.20-0.50")
    print("  Gemini:   ~$0.15-0.40")
    print("  GPT-4:    ~$15-20")
    print("  Claude:   ~$12-18")

import os
