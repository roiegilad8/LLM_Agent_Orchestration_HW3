"""Integration tests for full pipeline."""
import pytest
from src.agents.agent_chain import TranslationChain
from src.embeddings.similarity import SimilarityCalculator
from src.utils.error_injection import inject_errors


class TestIntegration:
    """Test full pipeline integration."""
    
    def test_full_translation_pipeline(self):
        """Test complete translation chain."""
        chain = TranslationChain()
        text = "Hello world"
        
        result = chain.run(text)
        
        assert "original" in result
        assert "stages" in result
        assert "final" in result
        assert len(result["stages"]) == 3
    
    def test_error_injection_pipeline(self):
        """Test pipeline with error injection."""
        chain = TranslationChain()
        calc = SimilarityCalculator()
        
        original = "The quick brown fox jumps over the lazy dog"
        corrupted = inject_errors(original, 0.5, seed=123)
        
        result = chain.run(corrupted)
        distance = calc.calculate_distance(original, result["final"])
        
        assert -0.01 <= distance <= 2.0
    
    def test_multiple_error_rates(self):
        """Test pipeline with different error rates."""
        chain = TranslationChain()
        calc = SimilarityCalculator()
        
        text = "Hello world"
        distances = []
        
        for error_rate in [0.0, 0.3]:
            corrupted = inject_errors(text, error_rate, seed=42)
            result = chain.run(corrupted)
            distance = calc.calculate_distance(text, result["final"])
            distances.append(distance)
        
        assert len(distances) == 2
        for d in distances:
            assert -0.01 <= d <= 1.0, f"Distance {d} out of range"
    
    def test_config_loading(self):
        """Test configuration loads correctly."""
        import yaml
        from pathlib import Path
        
        config_path = Path("config/config.yaml")
        assert config_path.exists()
        
        with open(config_path) as f:
            config = yaml.safe_load(f)
        
        assert "ollama" in config
        assert "experiment" in config
        assert "test_sentences" in config
