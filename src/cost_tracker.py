"""
Cost Tracker - Track API usage and costs
"""

class CostTracker:
    def __init__(self):
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        
        # DeepSeek pricing (per 1M tokens)
        self.input_cost_per_1m = 0.14
        self.output_cost_per_1m = 0.28
    
    def add_tokens(self, input_tokens: int, output_tokens: int):
        """Add tokens to the tracker."""
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
    
    def estimate_tokens(self, text: str, is_input: bool = True):
        """Estimate tokens from text (rough: 1 token ≈ 0.75 words)."""
        words = len(text.split())
        tokens = int(words / 0.75)
        
        if is_input:
            self.total_input_tokens += tokens
        else:
            self.total_output_tokens += tokens
        
        return tokens
    
    def get_cost(self) -> float:
        """Calculate total cost in USD."""
        input_cost = (self.total_input_tokens / 1_000_000) * self.input_cost_per_1m
        output_cost = (self.total_output_tokens / 1_000_000) * self.output_cost_per_1m
        return input_cost + output_cost
    
    def get_summary(self) -> dict:
        """Get summary of usage and cost."""
        return {
            'input_tokens': self.total_input_tokens,
            'output_tokens': self.total_output_tokens,
            'total_tokens': self.total_input_tokens + self.total_output_tokens,
            'cost_usd': self.get_cost()
        }
    
    def print_summary(self):
        """Print cost summary."""
        summary = self.get_summary()
        print(f"\n💰 Cost Summary:")
        print(f"   Input tokens:  {summary['input_tokens']:,}")
        print(f"   Output tokens: {summary['output_tokens']:,}")
        print(f"   Total tokens:  {summary['total_tokens']:,}")
        print(f"   Estimated cost: ${summary['cost_usd']:.4f}")

# Global tracker instance
cost_tracker = CostTracker()
