"""Tests for agent system."""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agents.translator_agent import (
    EnglishToFrenchAgent,
    FrenchToHebrewAgent,
    HebrewToEnglishAgent
)
from agents.agent_chain import TranslationChain


class TestTranslators:
    """Test individual translator agents."""
    
    def test_english_to_french_agent(self):
        """Test EN→FR translation."""
        agent = EnglishToFrenchAgent()
        result = agent.translate("Hello world")
        
        assert result['output'] != ""
        assert result['source_lang'] == 'en'
        assert result['target_lang'] == 'fr'
        assert result['agent'] == 'EnglishToFrenchAgent'
    
    def test_french_to_hebrew_agent(self):
        """Test FR→HE translation."""
        agent = FrenchToHebrewAgent()
        result = agent.translate("Bonjour le monde")
        
        assert result['output'] != ""
        assert result['source_lang'] == 'fr'
        assert result['target_lang'] == 'he'
    
    def test_hebrew_to_english_agent(self):
        """Test HE→EN translation."""
        agent = HebrewToEnglishAgent()
        result = agent.translate("שלום עולם")
        
        assert result['output'] != ""
        assert result['source_lang'] == 'he'
        assert result['target_lang'] == 'en'


class TestTranslationChain:
    """Test the full translation chain."""
    
    def test_chain_initialization(self):
        """Test chain initializes with 3 agents."""
        chain = TranslationChain()
        assert len(chain.agents) == 3
    
    def test_chain_run(self):
        """Test full chain execution."""
        chain = TranslationChain()
        text = "Hello world"
        result = chain.run(text)
        
        assert result['original'] == text
        assert result['final'] != ""
        assert len(result['stages']) == 3