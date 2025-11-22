"""Pytest fixtures for testing."""
import pytest
from unittest.mock import Mock, MagicMock
import numpy as np


@pytest.fixture
def mock_ollama_response():
    """Mock successful Ollama translation response."""
    return {
        "response": "Bonjour le monde",
        "model": "llama3.2:1b",
        "done": True
    }


@pytest.fixture
def mock_ollama_client(mock_ollama_response):
    """Mock Ollama client for testing without API calls."""
    mock_client = MagicMock()
    mock_client.generate.return_value = mock_ollama_response
    return mock_client


@pytest.fixture
def mock_embeddings():
    """Mock sentence embeddings for testing."""
    mock = Mock()
    # Return normalized embeddings
    mock.encode.return_value = np.array([[0.1, 0.2, 0.3, 0.4, 0.5]])
    return mock


@pytest.fixture
def sample_sentences():
    """Sample sentences for testing."""
    return [
        "Hello world",
        "This is a test",
        "Machine translation example"
    ]


@pytest.fixture
def mock_translator_responses():
    """Mock responses for multi-agent chain."""
    return {
        "en_to_fr": "Bonjour le monde",
        "fr_to_he": "שלום עולם",
        "he_to_en": "Hello world"
    }
