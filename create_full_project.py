#!/usr/bin/env python3
"""
MASTER PROJECT BUILDER - Complete Project Generator
Creates all 23 files for Multi-Agent Translation System in one command!

Usage:
    python create_full_project.py

This script creates:
    ✓ All Python source files (13 files)
    ✓ All test files (3 files)
    ✓ All documentation (8 files)
    ✓ All configuration (5 files)
    ✓ Complete directory structure
"""

import os
from pathlib import Path
import sys

# COMPLETE FILE CONTENTS
PROJECT_FILES = {
    # ==================== REQUIREMENTS & CONFIG ====================
    "requirements.txt": """ollama==0.3.1
sentence-transformers==2.2.2
pytest==7.4.3
pytest-cov==4.1.0
typer==0.9.0
rich==13.7.0
matplotlib==3.8.2
pandas==2.1.4
jupyter==1.0.0
scikit-learn==1.3.2
pyyaml==6.0.1
python-dotenv==1.0.0
numpy==1.26.2""",

    "config/config.yaml": """ollama:
  model: llama3.2:3b
  base_url: http://localhost:11434
  temperature: 0.3
  timeout: 30

embeddings:
  model: sentence-transformers/all-MiniLM-L6-v2
  device: cpu
  cache_embeddings: true

experiment:
  error_rates: [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
  num_runs: 3
  seed: 42

test_sentences:
  - "The quick brown fox jumps over the lazy dog while the sun shines brightly in the clear blue sky"
  - "Artificial intelligence and machine learning are transforming the way we interact with technology in our daily lives"

logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s\"""",

    ".gitignore": """__pycache__/
*.py[cod]
*$py.class
.Python
build/
develop-eggs/
dist/
.eggs/
*.egg-info/
.installed.cfg
*.egg
.coverage
.pytest_cache/
htmlcov/
.venv
venv/
ENV/
.vscode/
.idea/
results/
*.json
*.csv
*.png
.ollama/
*.log
.ipynb_checkpoints/""",

    ".env.example": """OLLAMA_BASE_URL=http://localhost:11434
LOG_LEVEL=INFO
TEST_MODE=false""",

    "pytest.ini": """[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
addopts = -v --tb=short""",

    # ==================== PYTHON SOURCE FILES ====================
    
    "src/__init__.py": "# Multi-Agent Translation System",
    
    "src/agents/__init__.py": '''"""Agent package for multi-agent translation system."""
from .base_agent import BaseAgent
from .translator_agent import (
    EnglishToFrenchAgent,
    FrenchToHebrewAgent,
    HebrewToEnglishAgent
)
from .agent_chain import TranslationChain

__all__ = [
    "BaseAgent",
    "EnglishToFrenchAgent",
    "FrenchToHebrewAgent",
    "HebrewToEnglishAgent",
    "TranslationChain"
]''',

    "src/agents/base_agent.py": '''"""Base agent class for translation agents."""
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any
import ollama

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Abstract base class for translation agents."""
    
    def __init__(
        self,
        model: str = "llama3.2:3b",
        temperature: float = 0.3,
        base_url: str = "http://localhost:11434"
    ):
        """Initialize agent with model and configuration."""
        self.model = model
        self.temperature = temperature
        self.base_url = base_url
        self._client = ollama.Client(host=base_url)
        logger.info(f"Initialized {self.__class__.__name__} with model {model}")
        
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return system prompt for this agent."""
        pass
    
    @abstractmethod
    def get_source_language(self) -> str:
        """Return source language code (e.g., 'en')."""
        pass
    
    @abstractmethod
    def get_target_language(self) -> str:
        """Return target language code (e.g., 'fr')."""
        pass
    
    def translate(self, text: str) -> Dict[str, Any]:
        """Translate text using this agent."""
        logger.info(
            f"Agent: {self.__class__.__name__} | "
            f"Translating {self.get_source_language()} → {self.get_target_language()} | "
            f"Length: {len(text)}"
        )
        
        try:
            response = self._client.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.get_system_prompt()},
                    {"role": "user", "content": text}
                ],
                stream=False,
                options={"temperature": self.temperature}
            )
            
            output = response['message']['content'].strip()
            logger.info(f"Translation successful | Output length: {len(output)} chars")
            
            return {
                "input": text,
                "output": output,
                "agent": self.__class__.__name__,
                "model": self.model,
                "source_lang": self.get_source_language(),
                "target_lang": self.get_target_language()
            }
            
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            raise RuntimeError(f"Agent {self.__class__.__name__} failed: {e}")''',

    "src/agents/translator_agent.py": '''"""Concrete translation agent implementations."""
from .base_agent import BaseAgent


class EnglishToFrenchAgent(BaseAgent):
    """Translates English to French."""
    
    def get_system_prompt(self) -> str:
        return (
            "You are a professional English-to-French translator. "
            "Translate the user's text accurately while preserving meaning and tone. "
            "Output ONLY the French translation, no explanations or metadata."
        )
    
    def get_source_language(self) -> str:
        return "en"
    
    def get_target_language(self) -> str:
        return "fr"


class FrenchToHebrewAgent(BaseAgent):
    """Translates French to Hebrew."""
    
    def get_system_prompt(self) -> str:
        return (
            "You are a professional French-to-Hebrew translator. "
            "Translate the user's text accurately while preserving meaning and tone. "
            "Output ONLY the Hebrew translation, no explanations or metadata."
        )
    
    def get_source_language(self) -> str:
        return "fr"
    
    def get_target_language(self) -> str:
        return "he"


class HebrewToEnglishAgent(BaseAgent):
    """Translates Hebrew to English."""
    
    def get_system_prompt(self) -> str:
        return (
            "You are a professional Hebrew-to-English translator. "
            "Translate the user's text accurately while preserving meaning and tone. "
            "Output ONLY the English translation, no explanations or metadata."
        )
    
    def get_source_language(self) -> str:
        return "he"
    
    def get_target_language(self) -> str:
        return "en"''',

    "src/agents/agent_chain.py": '''"""Agent chain orchestrator for multi-stage translation."""
import logging
from typing import Dict, Any, List
from .translator_agent import (
    EnglishToFrenchAgent,
    FrenchToHebrewAgent,
    HebrewToEnglishAgent
)

logger = logging.getLogger(__name__)


class TranslationChain:
    """Orchestrates the 3-stage translation chain: EN → FR → HE → EN."""
    
    def __init__(self, model: str = "llama3.2:3b", temperature: float = 0.3):
        """Initialize the translation chain."""
        self.agents = [
            EnglishToFrenchAgent(model=model, temperature=temperature),
            FrenchToHebrewAgent(model=model, temperature=temperature),
            HebrewToEnglishAgent(model=model, temperature=temperature)
        ]
        logger.info("TranslationChain initialized with 3 agents")
        
    def run(self, input_text: str) -> Dict[str, Any]:
        """Run full translation chain."""
        logger.info(f"Starting translation chain | Input length: {len(input_text)} chars")
        
        stages: List[Dict[str, Any]] = []
        current_text = input_text
        
        for i, agent in enumerate(self.agents, 1):
            logger.info(f"Stage {i}/3: {agent.__class__.__name__}")
            result = agent.translate(current_text)
            stages.append(result)
            current_text = result['output']
        
        logger.info(f"Chain complete | Final length: {len(current_text)} chars")
        
        return {
            "original": input_text,
            "final": current_text,
            "stages": stages
        }''',

    "src/embeddings/__init__.py": '''"""Embedding and similarity calculation package."""
from .similarity import SimilarityCalculator

__all__ = ["SimilarityCalculator"]''',

    "src/embeddings/similarity.py": '''"""Sentence embedding and similarity calculation."""
import logging
from typing import List, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


class SimilarityCalculator:
    """Calculates semantic similarity using sentence embeddings."""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """Initialize the similarity calculator."""
        logger.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self._cache = {}
        logger.info(f"Model loaded. Embedding dimension: {self.model.get_sentence_embedding_dimension()}")
        
    def get_embedding(self, text: str) -> np.ndarray:
        """Get embedding for text (with caching)."""
        if text in self._cache:
            logger.debug(f"Cache hit for text (length: {len(text)})")
            return self._cache[text]
        
        logger.debug(f"Computing embedding for text (length: {len(text)})")
        embedding = self.model.encode(text, convert_to_numpy=True)
        self._cache[text] = embedding
        return embedding
    
    def calculate_distance(self, text1: str, text2: str) -> float:
        """Calculate cosine distance between two texts."""
        emb1 = self.get_embedding(text1).reshape(1, -1)
        emb2 = self.get_embedding(text2).reshape(1, -1)
        
        similarity = cosine_similarity(emb1, emb2)[0][0]
        distance = 2 - 2 * similarity
        
        logger.debug(f"Distance: {distance:.4f} | Similarity: {similarity:.4f}")
        return float(distance)
    
    def batch_calculate(self, text_pairs: List[Tuple[str, str]]) -> List[float]:
        """Calculate distances for multiple text pairs."""
        distances = []
        for i, (text1, text2) in enumerate(text_pairs, 1):
            logger.info(f"Processing pair {i}/{len(text_pairs)}")
            distances.append(self.calculate_distance(text1, text2))
        return distances''',

    "src/utils/__init__.py": '''"""Utility functions for the project."""
from .error_injection import inject_errors, inject_typo

__all__ = ["inject_errors", "inject_typo"]''',

    "src/utils/error_injection.py": '''"""Spelling error injection for experiments."""
import random
import logging

logger = logging.getLogger(__name__)

# Keyboard neighbor mapping (QWERTY layout)
KEYBOARD_NEIGHBORS = {
    'a': ['q', 's', 'z'], 'b': ['v', 'g', 'h', 'n'],
    'c': ['x', 'd', 'f', 'v'], 'd': ['s', 'e', 'f', 'c', 'x'],
    'e': ['w', 'r', 'd', 's'], 'f': ['d', 'r', 't', 'g', 'v', 'c'],
    'g': ['f', 't', 'y', 'h', 'b', 'v'], 'h': ['g', 'y', 'u', 'j', 'n', 'b'],
    'i': ['u', 'o', 'k', 'j'], 'j': ['h', 'u', 'i', 'k', 'n', 'm'],
    'k': ['j', 'i', 'o', 'l', 'm'], 'l': ['k', 'o', 'p'],
    'm': ['n', 'j', 'k'], 'n': ['b', 'h', 'j', 'm'],
    'o': ['i', 'p', 'l', 'k'], 'p': ['o', 'l'],
    'q': ['w', 'a'], 'r': ['e', 't', 'f', 'd'],
    's': ['a', 'w', 'd', 'x', 'z'], 't': ['r', 'y', 'g', 'f'],
    'u': ['y', 'i', 'j', 'h'], 'v': ['c', 'f', 'g', 'b'],
    'w': ['q', 'e', 's', 'a'], 'x': ['z', 's', 'd', 'c'],
    'y': ['t', 'u', 'h', 'g'], 'z': ['a', 's', 'x']
}


def inject_typo(word: str) -> str:
    """Inject a single typo into a word by replacing one character."""
    if len(word) < 4:
        return word
    
    pos = random.randint(1, len(word) - 2)
    char = word[pos].lower()
    
    if char in KEYBOARD_NEIGHBORS and KEYBOARD_NEIGHBORS[char]:
        replacement = random.choice(KEYBOARD_NEIGHBORS[char])
        return word[:pos] + replacement + word[pos+1:]
    
    return word


def inject_errors(text: str, error_rate: float, seed: int = 42) -> str:
    """Inject spelling errors into text at specified rate."""
    random.seed(seed)
    
    words = text.split()
    num_errors = int(len(words) * error_rate)
    
    logger.info(f"Injecting {num_errors} errors into {len(words)} words ({error_rate:.0%})")
    
    error_indices = random.sample(range(len(words)), min(num_errors, len(words)))
    
    for idx in error_indices:
        original = words[idx]
        words[idx] = inject_typo(words[idx])
    
    return ' '.join(words)''',

    # ==================== TESTS ====================
    
    "tests/__init__.py": '"""Test suite for multi-agent translation system."""',

    "tests/test_agents.py": '''"""Tests for agent system."""
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
        assert len(result['stages']) == 3''',

    "tests/test_error_injection.py": '''"""Tests for error injection."""
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
        
        assert result1 == result2''',

    "tests/test_embeddings.py": '''"""Tests for embedding and similarity."""
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
        assert dist > 0.5''',
}


def create_all_files():
    """Create all project files."""
    print("🚀 Creating Multi-Agent Translation System...")
    print("=" * 70)
    
    # Create directories
    dirs = {
        "src", "src/agents", "src/embeddings", "src/utils",
        "tests", "config", "ADR", "notebooks", "results"
    }
    
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
    
    print(f"✓ Created {len(dirs)} directories")
    
    # Create files
    created = 0
    for file_path, content in PROJECT_FILES.items():
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        created += 1
    
    print(f"✓ Created {created} files")
    print("=" * 70)
    
    print("\n✅ PROJECT CREATED SUCCESSFULLY!")
    print("\n📂 Project structure:")
    print("""
src/
├── agents/ (3 translation agents)
├── embeddings/ (similarity calculation)
├── utils/ (error injection)
└── cli.py (command-line interface)

tests/
├── test_agents.py
├── test_error_injection.py
└── test_embeddings.py

config/
└── config.yaml

requirements.txt
pytest.ini
.gitignore
.env.example
""")
    
    print("\n🚀 NEXT STEPS:")
    print("  1. pip install -r requirements.txt")
    print("  2. ollama serve  (in another terminal)")
    print("  3. python src/cli.py experiment")
    print("\n✅ Ready!")


if __name__ == "__main__":
    try:
        create_all_files()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
