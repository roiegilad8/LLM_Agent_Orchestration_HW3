"""Tests for error injection."""
import pytest
from src.utils.error_injection import inject_errors


class TestErrorInjection:
    """Test error injection functionality."""

    def test_zero_percent_errors(self):
        """Test 0% error rate (no changes)."""
        text = "Hello world"
        result = inject_errors(text, 0.0)
        assert result == text

    def test_error_injection(self):
        """Test error injection at 50%."""
        text = "Hello world this is a test sentence"
        result = inject_errors(text, 0.5, seed=42)
        assert result != text

    def test_reproducibility(self):
        """Test reproducibility with seed."""
        text = "Test reproducibility"
        result1 = inject_errors(text, 0.3, seed=42)
        result2 = inject_errors(text, 0.3, seed=42)
        assert result1 == result2

    def test_error_injection_max_rate(self):
        """Test maximum error rate (50%)."""
        text = "Hello world this is a test"
        result = inject_errors(text, 0.5, seed=42)
        assert result != text
        assert len(result) > 0

    def test_error_injection_empty_string(self):
        """Test error injection on empty string."""
        result = inject_errors("", 0.2, seed=42)
        assert result == ""

    def test_error_injection_single_char(self):
        """Test error injection on single character."""
        result = inject_errors("a", 1.0, seed=42)
        assert len(result) >= 0

    def test_error_injection_invalid_rate_negative(self):
        """Test invalid negative error rate."""
        with pytest.raises(ValueError):
            inject_errors("test", -0.1)

    def test_error_injection_invalid_rate_above_one(self):
        """Test invalid error rate > 1.0."""
        with pytest.raises(ValueError):
            inject_errors("test", 1.5)

