"""Concrete translation agent implementations."""
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
        return "en"