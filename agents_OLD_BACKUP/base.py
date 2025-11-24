"""Base classes for translation agents."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class TranslationAgent(Protocol):
    """Protocol for translation agents."""

    source_language: str
    target_language: str

    def translate(self, text: str) -> str:
        """Translate the incoming text to the agent's target language."""


@dataclass
class AgentDescription:
    """Metadata that describes an agent."""

    name: str
    source_language: str
    target_language: str
    description: str
