"""Tests for embedding and similarity."""
import pytest
import sys
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from embeddings.similarity import SimilarityCalculator


class TestSimilarityCalculator:
    """Test sentence similarity calculation."""
    
    @pytest.fixture
    def calculator(self):
        """Create calculator instance."""
        return SimilarityCalculator()
    
    def test_embedding_shape(self, calculator):
        """Test embedding dimension."""
        emb = calculator.get_embedding("Hello world")
        assert emb.shape == (384,)
    
    def test_identical_strings(self, calculator):
        """Test distance for identical strings."""
        dist = calculator.calculate_distance("Hello world", "Hello world")
        assert dist < 0.01
    
    def test_different_strings(self, calculator):
        """Test distance for different strings."""
        dist = calculator.calculate_distance("Hello world", "Goodbye universe")
        assert dist > 0.5