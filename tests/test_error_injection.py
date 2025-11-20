"""Tests for error injection."""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.error_injection import inject_errors, inject_typo


class TestErrorInjection:
    """Test error injection functionality."""
    
    def test_zero_percent_errors(self):
        """Test 0% error rate (no changes)."""
        text = "Hello world"
        result = inject_errors(text, error_rate=0.0)
        assert result == text
    
    def test_error_injection(self):
        """Test error injection at 50%."""
        text = "The quick brown fox jumps"
        result = inject_errors(text, error_rate=0.5, seed=42)
        
        assert result != text
        assert len(result.split()) == len(text.split())
    
    def test_reproducibility(self):
        """Test reproducibility with seed."""
        text = "Hello world testing"
        result1 = inject_errors(text, error_rate=0.3, seed=42)
        result2 = inject_errors(text, error_rate=0.3, seed=42)
        
        assert result1 == result2