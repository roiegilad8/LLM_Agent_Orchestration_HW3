# Multi-Agent Translation Analysis System

**M.Sc. Data Science Assignment - November 2025**

**Course:** LLM Agent Orchestration

**Instructor:** Dr. Segal Yoram

**Authors:** Tom Ron, Igor Nazarenko, Roie Gilad

**Assignment:** Homework 3 - Multi-Agent Translation Analysis

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Ollama](https://img.shields.io/badge/Ollama-llama3.2:1b-green.svg)](https://ollama.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📋 Table of Contents

- [Executive Summary](#executive-summary)
- [Problem Statement](#problem-statement)
- [Key Features](#key-features)
- [Results & Achievements](#results--achievements)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [Documentation](#documentation)
- [Technical Architecture](#technical-architecture)
- [Testing](#testing)
- [CI/CD & DevOps](#cicd--devops)
- [Configuration](#configuration)
- [Quality Assurance](#quality-assurance)
- [Contributing](#contributing)
- [License & Attribution](#license--attribution)
- [References](#references)

---

## Executive Summary

This project implements a multi-agent translation analysis system that measures semantic drift across a three-stage translation pipeline: English → French → Hebrew → English. The system uses Ollama local LLMs with controlled error injection to study the relationship between spelling errors and semantic preservation.

### Key Achievements

- ✅ **Professional Architecture**: BaseAgent abstraction with AgentChain orchestration
- ✅ **Comprehensive Testing**: 43 tests achieving 83% code coverage
- ✅ **Cost Efficiency**: $0.00 operational cost using local Ollama models
- ✅ **Complete Documentation**: PRD, 3 ADRs, Analysis Notebook, Professional README
- ✅ **Production-Ready**: CI/CD pipeline, mocking fixtures, cost tracking
- ✅ **Assignment Complete**: All requirements met and exceeded

### Innovation Highlight

The project demonstrates professional software engineering practices with Ollama API mocking via pytest fixtures, reducing test execution time from 20 minutes to 30 seconds while ensuring 100% reproducibility. The CI/CD pipeline with GitHub Actions enforces code quality standards automatically.

---

## Problem Statement

### Challenge

Given a sentence in English, translate it through a multi-language chain (EN → FR → HE → EN) while injecting controlled spelling errors, then measure the semantic drift from the original text.

### Task Specifications

**Translation Chain**: English → French → Hebrew → English  
**Error Rates**: 0%, 10%, 20%, 30%, 40%, 50%  
**Test Sentences**: 3 sentences (15+ words each)  
**Repetitions**: 3 runs per configuration  
**Total Experiments**: 54 translation chains

### Mathematical Formulation

For semantic distance measurement:

```
Cosine Distance = 1 - (v₁ · v₂) / (||v₁|| ||v₂||)
```

Where `v₁` is the original English embedding and `v₂` is the final translated embedding using Sentence-BERT (all-MiniLM-L6-v2).

**Error Injection**: Character-level substitution, deletion, and insertion at configurable rates while preserving word boundaries.

---

## Key Features

### Multi-Agent Architecture

1. **BaseAgent (Abstract)**
   - Defines consistent agent interface
   - Enforces process() method contract
   - Enables dependency injection for testing

2. **TranslatorAgent (Concrete)**
   - Uses Ollama (llama3.2:1b) for translation
   - Supports EN↔FR, EN↔HE, FR↔HE language pairs
   - Configurable temperature and prompting

3. **AgentChain (Orchestrator)**
   - Manages sequential agent execution
   - Handles error propagation
   - Tracks intermediate results

### Technical Excellence

- **GPU/CPU Support**: Automatic device detection for embeddings
- **Robust Error Handling**: Comprehensive validation and informative errors
- **Rich Visualizations**: Error impact analysis, distributions, box plots
- **Production-Ready**: Modular code, extensive testing, complete documentation

### Assignment Compliance

- ✅ Implements multi-agent orchestration with BaseAgent pattern
- ✅ Measures semantic distance using Sentence-BERT embeddings
- ✅ Tests multiple error rates (0% through 50%)
- ✅ Performs statistical analysis (mean, std, correlations)
- ✅ Generates comprehensive visualizations
- ✅ Includes PRD with requirements and KPIs
- ✅ Documents architectural decisions (3 ADRs)
- ✅ Achieves >70% test coverage (83%)
- ✅ Provides complete Git repository with meaningful commits

### Production-Ready Enhancements

This implementation includes professional software engineering practices:

#### Testing & CI/CD
- **Pytest Fixtures**: Mock Ollama API responses for deterministic testing
- **GitHub Actions**: Automated testing on every push with coverage enforcement
- **Test Coverage**: 83% coverage across all modules (43 tests)
- **Fast Tests**: 30-second execution vs. 20 minutes with live API

#### Cost Tracking
- **CostTracker Utility**: Monitors API calls, tokens, and runtime
- **Resource Documentation**: Disk space, RAM, CPU utilization detailed in README
- **Zero-Cost Operation**: Fully local execution with Ollama

#### Code Quality
- **Type Hints**: Throughout codebase for static analysis
- **Error Handling**: Comprehensive validation with clear messages
- **CLI Interface**: Typer-based CLI with Rich formatting
- **Configuration**: YAML-based configuration management

---

## Results & Achievements

### Performance Metrics

**Latest Experimental Run** (November 22, 2025):

| Metric | Value | Status |
|--------|-------|--------|
| **Test Coverage** | 83% | ✅ Excellent |
| **Total Tests** | 43 | ✅ Comprehensive |
| **Execution Time** | 20-25 min | ✅ Reasonable |
| **Operational Cost** | $0.00 | ✅ Zero |
| **Git Commits** | 10 | ✅ Good |
| **Documentation Files** | 12 | ✅ Complete |

### Semantic Distance Analysis

| Error Rate | Mean Distance | Std Dev | Interpretation |
|------------|---------------|---------|----------------|
| 0% | 0.05 | 0.02 | Baseline drift (translation ambiguity) |
| 10% | 0.12 | 0.04 | Minimal impact |
| 20% | 0.23 | 0.06 | Moderate impact |
| 30% | 0.38 | 0.09 | Significant drift |
| 40% | 0.52 | 0.11 | Major degradation |
| 50% | 0.71 | 0.14 | Severe failure |

### Key Findings

- **Linear Relationship**: Error rate correlates linearly with semantic distance
- **Critical Threshold**: 30% error rate where distance exceeds 0.35
- **System Resilience**: Remains partially functional up to 40% errors
- **Baseline Noise**: ~0.05 distance even at 0% errors due to translation ambiguity

### Visual Results

All figures available in `results/`:

- `error_impact_detailed.png` - Main analysis graph
- `distance_distributions.png` - Distribution histograms
- `distance_boxplot.png` - Box plot comparison

---

## Project Structure

```
LLM_HW3/
├── README.md                          # This file - comprehensive project guide
├── PRD.md                             # Product Requirements Document
├── requirements.txt                   # Python dependencies
├── pytest.ini                         # Test configuration
├── .gitignore                         # Git ignore patterns
│
├── ADR/                               # Architecture Decision Records
│   ├── ADR-001-agent-architecture.md  # Multi-agent design pattern
│   ├── ADR-002-embedding-model.md     # Sentence-BERT selection
│   └── ADR-003-error-injection.md     # Error injection methodology
│
├── src/                               # Source code
│   ├── agents/
│   │   ├── base_agent.py             # Abstract base class
│   │   ├── translator_agent.py       # Ollama-based translator
│   │   └── agent_chain.py            # Orchestration logic
│   ├── embeddings/
│   │   └── similarity.py             # Sentence embedding & distance
│   ├── utils/
│   │   ├── error_injection.py        # Spelling error generation
│   │   └── cost_tracker.py           # API usage tracking
│   └── cli.py                         # Command-line interface
│
├── tests/                             # Comprehensive test suite
│   ├── conftest.py                   # Pytest fixtures & mocking
│   ├── test_agents.py                # Agent tests (16 tests)
│   ├── test_error_injection.py       # Error injection tests (14 tests)
│   ├── test_embeddings.py            # Embedding tests (8 tests)
│   └── test_cost_tracker.py          # Cost tracker tests (5 tests)
│
├── config/
│   └── config.yaml                   # Experiment configuration
│
├── notebooks/
│   └── experiment_analysis.ipynb     # Data analysis & visualization
│
├── .github/workflows/
│   └── test.yml                      # CI/CD pipeline
│
└── results/
    ├── experiment.json               # Experimental results
    ├── error_impact_detailed.png
    ├── distance_distributions.png
    └── distance_boxplot.png
```

### File Organization Principles

Following software engineering best practices:

- **Separation of Concerns**: Data, agents, embeddings in separate modules
- **Modular Design**: Each module has single, well-defined responsibility
- **Clear Naming**: Descriptive file and function names throughout
- **Documentation First**: Every component fully documented
- **Test Coverage**: Comprehensive test suite covering all modules

---

## Installation

### Prerequisites

- **Python**: 3.10 or higher
- **pip**: Latest version recommended
- **OS**: Windows, macOS, or Linux

### Install Ollama

**On Linux/WSL:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**On macOS:**
```bash
brew install ollama
```

**On Windows:**
Download from [ollama.com/download](https://ollama.com/download)

**Pull the required model:**
```bash
ollama pull llama3.2:1b
```

**Verify installation:**
```bash
ollama --version
ollama list  # Should show llama3.2:1b
```

### Setup Steps

#### Step 1: Clone Repository

```bash
git clone https://github.com/roiegilad8/LLM_Agent_Orchestration_HW3.git
cd LLM_Agent_Orchestration_HW3
```

#### Step 2: Create Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

#### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Required Packages

```
typer>=0.9.0              # CLI framework
rich>=13.0.0              # Terminal output
sentence-transformers     # Embeddings
transformers              # NLP utilities
scipy                     # Statistics
pandas                    # Data manipulation
matplotlib                # Visualization
pyyaml                    # Configuration
pytest>=7.3.0             # Testing
pytest-cov>=4.1.0         # Coverage
```

#### Step 4: Verify Installation

```bash
# Start Ollama
ollama serve &

# Run tests
pytest -v

# Check coverage
pytest --cov=src --cov-report=term
```

---

## Quick Start

### Option 1: Single Translation (2 minutes)

Test a single translation with error injection:

```bash
python src/cli.py translate "The quick brown fox jumps over the lazy dog" --error-rate 0.2
```

### Option 2: Full Experiment (25 minutes)

Run complete experiments across all error rates:

```bash
python src/cli.py experiment
```

This will:
- Load test sentences from `config/config.yaml`
- Run translations for 6 error rates (0% through 50%)
- Perform 3 repetitions per configuration
- Save results to `results/experiment.json`

### Option 3: Analyze Results

Generate visualizations from experimental data:

```bash
python src/cli.py analyze results/experiment.json
```

Outputs:
- `error_impact_detailed.png`
- `distance_distributions.png`
- `distance_boxplot.png`

### Option 4: Interactive Exploration

Launch Jupyter notebook:

```bash
jupyter notebook notebooks/experiment_analysis.ipynb
```

---

## Usage Guide

### Command-Line Interface

```bash
python src/cli.py [COMMAND] [OPTIONS]
```

### Commands

#### 1. translate

Translate a single sentence:

```bash
python src/cli.py translate "Your sentence here" --error-rate 0.3 --seed 42
```

**Options:**
- `text`: Sentence to translate (required)
- `--error-rate`: Error injection rate (0.0-0.5, default: 0.0)
- `--seed`: Random seed for reproducibility (default: 42)

#### 2. experiment

Run full experimental suite:

```bash
python src/cli.py experiment
```

Configuration via `config/config.yaml`:
```yaml
experiment:
  error_rates: [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
  num_runs: 3
  seed: 42

test_sentences:
  - "Your first sentence (15+ words)"
  - "Your second sentence (15+ words)"
  - "Your third sentence (15+ words)"
```

#### 3. analyze

Generate visualizations:

```bash
python src/cli.py analyze results/experiment.json
```

### Usage Examples

#### Example 1: Test Different Error Rates

```bash
# No errors
python src/cli.py translate "Hello world" --error-rate 0.0

# 20% errors
python src/cli.py translate "Hello world" --error-rate 0.2

# Maximum errors
python src/cli.py translate "Hello world" --error-rate 0.5
```

#### Example 2: Custom Experiment Configuration

Edit `config/config.yaml`:

```yaml
experiment:
  error_rates: [0.0, 0.25, 0.5]  # Test only 3 rates
  num_runs: 5                     # More repetitions
  seed: 123                       # Different seed
```

Then run:

```bash
python src/cli.py experiment
```

---

## Documentation

This project includes comprehensive documentation:

### Core Documentation

1. **[Product Requirements Document (PRD.md)](PRD.md)**
   - Complete requirements and specifications
   - Success criteria and KPIs
   - Stakeholder identification
   - Technical constraints

2. **[ADR-001: Agent Architecture](ADR/ADR-001-agent-architecture.md)**
   - Multi-agent design pattern rationale
   - BaseAgent abstraction justification
   - Alternative approaches considered

3. **[ADR-002: Embedding Model](ADR/ADR-002-embedding-model.md)**
   - Sentence-BERT selection rationale
   - Multilingual support (101 languages)
   - Performance vs. cost trade-offs

4. **[ADR-003: Error Injection](ADR/ADR-003-error-injection.md)**
   - Character-level injection strategy
   - Language-agnostic approach
   - Reproducibility considerations

### Analysis Documentation

5. **[Experiment Analysis Notebook](notebooks/experiment_analysis.ipynb)**
   - Statistical analysis of results
   - Visualization generation
   - Mathematical derivations
   - Interpretation guide

### API Documentation

All modules include comprehensive docstrings:

```python
# Example from src/agents/base_agent.py
class BaseAgent(ABC):
    """Abstract base class for all agents in the system.

    This class defines the interface that all concrete agents must implement,
    ensuring consistent behavior and enabling dependency injection for testing.

    Attributes:
        name (str): Human-readable name of the agent

    Methods:
        process(input_data: str) -> str: Process input and return output
    """
```

---

## Technical Architecture

### System Overview

```
Input: English Sentence + Error Rate
   ↓
Error Injection (character-level)
   ↓
Agent 1: EN → FR (Ollama)
   ↓
Agent 2: FR → HE (Ollama)
   ↓
Agent 3: HE → EN (Ollama)
   ↓
Semantic Distance: Cosine(Original, Final)
```

### Multi-Agent Design Pattern

**BaseAgent (Abstract)**

```python
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    @abstractmethod
    def process(self, input_data: str) -> str:
        """Process input and return output."""
        pass
```

**TranslatorAgent (Concrete)**

```python
class TranslatorAgent(BaseAgent):
    def __init__(self, ollama_client, source_lang, target_lang):
        self.client = ollama_client
        self.source = source_lang
        self.target = target_lang

    def process(self, text: str) -> str:
        prompt = f"Translate from {self.source} to {self.target}: {text}"
        response = self.client.generate(model="llama3.2:1b", prompt=prompt)
        return response['response']
```

**AgentChain (Orchestrator)**

```python
class AgentChain:
    def __init__(self, agents: List[BaseAgent]):
        self.agents = agents

    def execute(self, initial_input: str) -> List[str]:
        results = [initial_input]
        current = initial_input
        for agent in self.agents:
            current = agent.process(current)
            results.append(current)
        return results
```

### Semantic Distance Calculation

Using Sentence-BERT (all-MiniLM-L6-v2):

```python
from sentence_transformers import SentenceTransformer
import numpy as np

class SimilarityCalculator:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def calculate_distance(self, text1: str, text2: str) -> float:
        """Calculate cosine distance between two texts."""
        embeddings = self.model.encode([text1, text2])
        similarity = np.dot(embeddings[0], embeddings[1]) / (
            np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
        )
        distance = 1 - similarity  # Convert to distance
        return float(distance)
```

### Key Design Decisions

1. **Dependency Injection**: Ollama client injected into agents for testability
2. **Stateless Agents**: Each agent is stateless, simplifying testing and scaling
3. **Chain of Responsibility**: AgentChain implements this pattern for orchestration
4. **Separation of Concerns**: Clear boundaries between agents, embeddings, utilities

---

## Testing

### Comprehensive Test Suite

43 tests across 5 modules achieving 83% coverage:

```bash
# Run all tests
pytest -v

# Run specific modules
pytest tests/test_agents.py -v
pytest tests/test_error_injection.py -v
pytest tests/test_embeddings.py -v
pytest tests/test_cost_tracker.py -v

# Run with coverage
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

### Test Coverage Breakdown

| Module | Tests | Coverage | Status |
|--------|-------|----------|--------|
| **Agents** | 16 | 85% | ✅ |
| **Error Injection** | 14 | 92% | ✅ |
| **Embeddings** | 8 | 78% | ✅ |
| **Cost Tracker** | 5 | 88% | ✅ |
| **Total** | **43** | **83%** | ✅ |

### Mocking Architecture

Professional pytest fixtures in `tests/conftest.py`:

```python
@pytest.fixture
def mock_ollama_client(mock_ollama_response):
    """Mock Ollama client for testing without API calls."""
    mock_client = MagicMock()
    mock_client.generate.return_value = mock_ollama_response
    return mock_client

@pytest.fixture
def mock_ollama_response():
    """Standard Ollama response for testing."""
    return {
        'response': 'Mocked translation result',
        'model': 'llama3.2:1b',
        'created_at': '2025-11-22T00:00:00Z'
    }
```

**Benefits:**
- Test execution: 30 seconds (vs. 20 minutes with live API)
- 100% reproducible results
- No external dependencies
- CI/CD compatible

---

## CI/CD & DevOps

### GitHub Actions Workflow

`.github/workflows/test.yml`:

```yaml
name: Tests and Coverage

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run tests with coverage
      run: |
        pytest --cov=src --cov-report=term --cov-report=xml

    - name: Check coverage threshold
      run: |
        python -m coverage report --fail-under=80

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: false
```

### Cost Tracking System

`src/utils/cost_tracker.py`:

```python
@dataclass
class CostTracker:
    """Track API usage and estimated costs."""

    total_calls: int = 0
    total_tokens: int = 0
    start_time: datetime = field(default_factory=datetime.now)

    # Ollama is free, but track usage
    COST_PER_1K_TOKENS = 0.0

    def log_call(self, tokens: int = 100):
        """Log an API call."""
        self.total_calls += 1
        self.total_tokens += tokens

    def get_summary(self) -> Dict:
        """Get cost summary."""
        runtime = (datetime.now() - self.start_time).total_seconds()
        return {
            "total_calls": self.total_calls,
            "total_tokens": self.total_tokens,
            "estimated_cost_usd": self.total_tokens / 1000 * self.COST_PER_1K_TOKENS,
            "runtime_seconds": runtime
        }
```

### Resource Usage Documentation

| Component | Provider | Cost |
|-----------|----------|------|
| Translation (llama3.2:1b) | Ollama (local) | $0.00 |
| Embeddings (all-MiniLM-L6-v2) | sentence-transformers | $0.00 |
| **Total** | - | **$0.00** |

**Resource Requirements:**
- Disk Space: ~2GB for Ollama models
- RAM: ~4GB during experiments
- Runtime: 20-25 minutes for full experiments
- CPU: Utilizes 4-8 cores during translation

---

## Configuration

### YAML Configuration

`config/config.yaml`:

```yaml
ollama:
  model: llama3.2:1b
  base_url: http://localhost:11434
  temperature: 0.3

experiment:
  error_rates: [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
  num_runs: 3
  seed: 42

test_sentences:
  - "The quick brown fox jumps over the lazy dog in the forest"
  - "Machine learning algorithms process data to make predictions"
  - "Climate change affects ecosystems around the world significantly"

embedding:
  model: all-MiniLM-L6-v2
  device: auto  # auto, cpu, cuda, mps
```

### Reproducibility

All results are fully reproducible:

```bash
# Exact reproduction of results
python src/cli.py experiment --seed 42
```

All random seeds are fixed:
- Experiment seed: 42
- Error injection: Per-run seeds
- Torch/NumPy: Environment variables

---

## Quality Assurance

### Code Quality Standards

- **PEP 8**: Python style guide compliance
- **Type Hints**: Full type annotations throughout
- **Docstrings**: Comprehensive documentation for all public APIs
- **DRY Principle**: No code duplication
- **SOLID Principles**: Clean architecture and design

### Testing Standards

- ✅ Unit tests for all modules
- ✅ Integration tests for complete pipeline
- ✅ Edge case coverage
- ✅ 83% code coverage (exceeds 70% requirement)
- ✅ Automated testing via GitHub Actions

### Documentation Standards

- ✅ Comprehensive README (this file)
- ✅ Architecture documentation (ADRs)
- ✅ API documentation (docstrings)
- ✅ Analysis notebook with explanations
- ✅ Configuration examples

---

## Contributing

### Development Setup

1. Fork the repository
2. Create virtual environment and install dependencies
3. Create feature branch: `git checkout -b feature/amazing-feature`
4. Make changes and add tests
5. Run tests: `pytest -v`
6. Commit changes: `git commit -m "Add amazing feature"`
7. Push to branch: `git push origin feature/amazing-feature`
8. Open Pull Request

### Code Style Guidelines

- Follow PEP 8
- Add type hints
- Write docstrings (Google style)
- Add unit tests for new features
- Update documentation

### Testing Requirements

All contributions must:
- Pass existing tests
- Add new tests for new features
- Maintain >80% code coverage
- Pass CI/CD pipeline

---

## License & Attribution

### License

This project is developed for educational purposes as part of M.Sc. Data Science coursework.

**Course:** LLM Agent Orchestration  
**Assignment:** Homework 3 - Multi-Agent Translation Analysis  
**Date:** November 2025

### Authors

- **Tom Ron** - ID 301020723
- **Igor Nazarenko** - ID 322029158
- **Roie Gilad** - ID 312169543

### Acknowledgments

- Course instructors for guidance and requirements
- Ollama team for local LLM infrastructure
- Sentence-Transformers team for multilingual embeddings
- PyTorch and Hugging Face communities

### Third-Party Libraries

- Ollama (MIT License)
- Sentence-Transformers (Apache 2.0)
- PyTorch (BSD License)
- Typer (MIT License)
- pytest (MIT License)

### Citation

If you use this code or methodology in your research, please cite:

```bibtex
@software{multiagent_translation_2025,
  author = {Ron, Tom and Nazarenko, Igor and Gilad, Roie},
  title = {Multi-Agent Translation Analysis System},
  year = {2025},
  course = {LLM Agent Orchestration},
  assignment = {Homework 3},
  url = {https://github.com/roiegilad8/LLM_Agent_Orchestration_HW3}
}
```

---

## References

### Academic References

1. **Reimers, N., & Gurevych, I. (2019)**. Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. *EMNLP 2019*.  
   arXiv: [1908.10084](https://arxiv.org/abs/1908.10084)

2. **Vaswani, A., et al. (2017)**. Attention Is All You Need. In *NIPS 2017*.  
   arXiv: [1706.03762](https://arxiv.org/abs/1706.03762)

3. **Devlin, J., et al. (2019)**. BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. In *NAACL 2019*.  
   arXiv: [1810.04805](https://arxiv.org/abs/1810.04805)

### Technical References

4. **Ollama Documentation**: https://ollama.com/docs
5. **Sentence-Transformers Documentation**: https://www.sbert.net/
6. **PyTorch Documentation**: https://pytorch.org/docs/

### Project Documentation

7. **[Product Requirements Document](PRD.md)** - Complete project requirements
8. **[ADR-001](ADR/ADR-001-agent-architecture.md)** - Agent architecture decisions
9. **[ADR-002](ADR/ADR-002-embedding-model.md)** - Embedding model selection
10. **[ADR-003](ADR/ADR-003-error-injection.md)** - Error injection methodology

---

## Support & Contact

### Getting Help

1. **Read Documentation**: Start with this README and linked docs
2. **Check Issues**: Review existing issues on GitHub
3. **Run Tests**: `pytest -v` to verify setup
4. **Review Code**: All modules include extensive comments

### Troubleshooting

**Ollama not running:**
```bash
ollama serve
```

**Model not found:**
```bash
ollama pull llama3.2:1b
```

**Config file not found:**
```bash
# Ensure you're in project root
cd ~/LLM_HW3
python src/cli.py experiment
```

**Permission denied on push:**
Create a Personal Access Token on GitHub with `repo` scope and use as password.

---

## Final Notes

This project demonstrates professional software engineering practices in the context of LLM agent orchestration. The system achieves:

- **Zero operational cost** through local Ollama execution
- **High reliability** through comprehensive testing and mocking
- **Production readiness** through CI/CD and quality assurance
- **Clear documentation** through PRD, ADRs, and analysis notebooks

We hope this project serves as:
- A complete solution to the assignment requirements
- A demonstration of multi-agent design patterns
- An example of professional software development practices
- A reference for future LLM orchestration projects

**Thank you for reviewing our work!**

---

**Last Updated:** November 22, 2025  
**Version:** 1.0.0  
**Status:** Ready for Submission ✅  
**Repository:** https://github.com/roiegilad8/LLM_Agent_Orchestration_HW3

---
