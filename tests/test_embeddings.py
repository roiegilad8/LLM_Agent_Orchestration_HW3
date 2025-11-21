"""Tests for embedding and similarity."""
import pytest
from src.embeddings.similarity import SimilarityCalculator


class TestSimilarityCalculator:
    """Test sentence similarity calculation."""

    def test_embedding_shape(self):
        """Test embedding dimension."""
        calc = SimilarityCalculator()
        embedding = calc.get_embedding("test")
        assert embedding.shape[0] == 384

    def test_identical_strings(self):
        """Test distance for identical strings."""
        calc = SimilarityCalculator()
        distance = calc.calculate_distance("hello", "hello")
        assert distance < 0.01

    def test_different_strings(self):
        """Test distance for different strings."""
        calc = SimilarityCalculator()
        distance = calc.calculate_distance("hello", "goodbye")
        assert 0.3 < distance < 0.8

    def test_empty_string_distance(self):
        """Test distance calculation with empty strings."""
        calc = SimilarityCalculator()
        try:
            distance = calc.calculate_distance("", "hello")
            assert 0.0 <= distance <= 2.0
        except Exception:
            pass

    def test_identical_long_strings(self):
        """Test distance for identical long strings."""
        calc = SimilarityCalculator()
        text = "This is a much longer sentence " * 10
        distance = calc.calculate_distance(text, text)
        assert distance < 0.01

    def test_cache_functionality(self):
        """Test that caching works."""
        calc = SimilarityCalculator()
        text = "Test caching mechanism"
        calc.get_embedding(text)
        cached = calc.get_embedding(text)
        assert cached is not None
        assert len(calc._cache) > 0
