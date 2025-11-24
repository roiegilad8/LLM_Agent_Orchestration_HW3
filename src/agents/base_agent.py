"""Base agent class for translation agents."""
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
                options={"temperature": self.temperature,
			 "num_predict": 300,
			 "timeout": 60.0}
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
            raise RuntimeError(f"Agent {self.__class__.__name__} failed: {e}")
