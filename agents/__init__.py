"""Agent package for translation pipeline."""

from .base import TranslationAgent
from .dictionary_agent import DictionaryTranslationAgent

__all__ = ["TranslationAgent", "DictionaryTranslationAgent"]
