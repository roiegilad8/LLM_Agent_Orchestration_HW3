"""Track API costs for Ollama calls."""
from dataclasses import dataclass, field
from typing import Dict
from datetime import datetime


@dataclass
class CostTracker:
    """Track API usage and estimated costs."""
    
    total_calls: int = 0
    total_tokens: int = 0
    start_time: datetime = field(default_factory=datetime.now)
    
    # Ollama is free, but track usage
    COST_PER_1K_TOKENS = 0.0
    
    def log_call(self, tokens: int = 100):
        """Log an API call.
        
        Args:
            tokens: Estimated tokens used (default: 100)
        """
        self.total_calls += 1
        self.total_tokens += tokens
    
    def get_summary(self) -> Dict:
        """Get cost summary.
        
        Returns:
            Dictionary with usage statistics
        """
        runtime = (datetime.now() - self.start_time).total_seconds()
        return {
            "total_calls": self.total_calls,
            "total_tokens": self.total_tokens,
            "estimated_cost_usd": self.total_tokens / 1000 * self.COST_PER_1K_TOKENS,
            "runtime_seconds": runtime
        }
    
    def reset(self):
        """Reset tracker."""
        self.total_calls = 0
        self.total_tokens = 0
        self.start_time = datetime.now()
    
    def __str__(self) -> str:
        """Human-readable summary."""
        summary = self.get_summary()
        return (
            f"📊 API Usage Summary\n"
            f"{'='*40}\n"
            f"Total Calls:     {summary['total_calls']}\n"
            f"Total Tokens:    {summary['total_tokens']:,}\n"
            f"Estimated Cost:  ${summary['estimated_cost_usd']:.4f}\n"
            f"Runtime:         {summary['runtime_seconds']:.1f}s\n"
            f"{'='*40}"
        )


# Global tracker instance
tracker = CostTracker()
