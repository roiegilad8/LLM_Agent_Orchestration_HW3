"""Dictionary-backed translation agent implementations."""
from __future__ import annotations

import difflib
import re
from dataclasses import dataclass
from typing import Dict

from .base import AgentDescription, TranslationAgent

_WORD_RE = re.compile(r"(\w+|[^\w\s])", re.UNICODE)


@dataclass
class DictionaryTranslationAgent:
    """Translate text using a simple dictionary with fuzzy matching."""

    name: str
    source_language: str
    target_language: str
    dictionary: Dict[str, str]
    description: str

    def translate(self, text: str) -> str:
        tokens = _WORD_RE.findall(text)
        translated_tokens = [self._translate_token(token) for token in tokens]
        return self._reconstruct_text(tokens, translated_tokens)

    def _translate_token(self, token: str) -> str:
        lower = token.lower()
        if lower in self.dictionary:
            return self.dictionary[lower]

        if lower.strip() == "":
            return token

        candidates = difflib.get_close_matches(lower, self.dictionary.keys(), n=1, cutoff=0.75)
        if candidates:
            return self.dictionary[candidates[0]]
        return token

    @staticmethod
    def _reconstruct_text(original_tokens, translated_tokens) -> str:
        pieces = []
        for original, translated in zip(original_tokens, translated_tokens):
            if translated is None:
                translated = original

            if any(ch.isalnum() for ch in original):
                pieces.append(translated)
            else:
                pieces.append(translated if translated != original else original)

        text = ""
        for piece in pieces:
            if not piece:
                continue
            if not text:
                text = piece
                continue
            if any(ch.isalnum() for ch in piece):
                text += " " + piece
            else:
                text = text.rstrip() + piece
        return text.strip()

    def describe(self) -> AgentDescription:
        return AgentDescription(
            name=self.name,
            source_language=self.source_language,
            target_language=self.target_language,
            description=self.description,
        )
