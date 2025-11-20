"""Agent chain orchestrator for multi-stage translation."""
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
        }