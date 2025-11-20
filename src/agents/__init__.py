"""Agent package for multi-agent translation system."""
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
]