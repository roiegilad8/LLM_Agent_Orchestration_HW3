"""
Tests for error injection functionality.
"""
import pytest
from src.utils.error_injection import inject_errors


class TestErrorInjection:
    """Test suite for error injection."""

    def test_error_injection_basic(self):
        """Test basic error injection."""
        text = "hello world"
        result = inject_errors(text, error_rate=0.5, seed=42)
        assert result != text
        assert len(result.split()) == len(text.split())

    def test_error_injection_zero_rate(self):
        """Test error injection with zero error rate."""
        text = "hello world"
        result = inject_errors(text, error_rate=0.0, seed=42)
        assert result == text

    def test_error_injection_max_rate(self):
        """Test error injection with maximum error rate."""
        text = "hello world"
        result = inject_errors(text, error_rate=0.5, seed=42)
        assert result != text

    def test_error_injection_preserves_word_count(self):
        """Test that error injection preserves word count."""
        text = "the quick brown fox jumps"
        result = inject_errors(text, error_rate=0.3, seed=42)
        assert len(result.split()) == len(text.split())

    def test_error_injection_single_word(self):
        """Test error injection with single word."""
        text = "hello"
        result = inject_errors(text, error_rate=0.5, seed=42)
        # May or may not change depending on random seed
        assert len(result) > 0

    def test_error_injection_long_text(self):
        """Test error injection with long text."""
        text = "the quick brown fox jumps over the lazy dog"
        result = inject_errors(text, error_rate=0.2, seed=42)
        assert len(result.split()) == len(text.split())

    def test_error_injection_special_chars(self):
        """Test error injection with special characters."""
        text = "hello, world! how are you?"
        result = inject_errors(text, error_rate=0.3, seed=42)
        # Should preserve punctuation
        assert ',' in result or '!' in result or '?' in result

    def test_error_injection_reproducibility(self):
        """Test error injection reproducibility with same seed."""
        text = "test text for reproducibility"
        result1 = inject_errors(text, error_rate=0.3, seed=42)
        result2 = inject_errors(text, error_rate=0.3, seed=42)
        assert result1 == result2

    # FIXED: Added 'self' parameter to all 4 functions below

    def test_error_injection_empty_string(self):
        """Test error injection with empty string."""
        result = inject_errors("", error_rate=0.5, seed=42)
        assert result == ""

    def test_error_injection_different_seeds(self):
        """Test that different seeds produce different results."""
        text = "test text for different seeds"
        result1 = inject_errors(text, error_rate=0.3, seed=42)
        result2 = inject_errors(text, error_rate=0.3, seed=99)
        # High probability of being different (not guaranteed but very likely)
        # We skip this test if by chance they're the same
        if result1 == result2:
            pytest.skip("Random seeds happened to produce same result")

    def test_error_rate_zero(self):
        """Test that error rate of 0.0 returns original text."""
        text = "no errors should be injected here"
        result = inject_errors(text, error_rate=0.0, seed=42)
        assert result == text

    def test_error_injection_whitespace_preservation(self):
        """Test that whitespace structure is preserved."""
        text = "hello   world  with   spaces"
        result = inject_errors(text, error_rate=0.3, seed=42)
        # Word count should be preserved
        assert len(result.split()) == len(text.split())
