# Multi-Agent Translation Analysis System

## Overview

This project implements a multi-agent translation pipeline involving English, French, and Hebrew. It evaluates the impact of spelling errors on semantic drift through a three-stage translation chain.

The system uses Ollama local LLMs to perform sequential translations while injecting controlled spelling errors to measure semantic preservation across languages.

## Features

- **Three Translation Agents** (EN → FR → HE → EN) using Ollama LLMs
- **Error Injection System** with configurable error rates (0% to 50%)
- **Semantic Distance Calculation** using Sentence-Transformers embeddings
- **Command-Line Interface** with 3 main commands (translate, experiment, analyze)
- **Comprehensive Test Suite** with 95% code coverage (22 tests)
- **Advanced Analysis** with Jupyter notebook for statistical insights
- **Professional Documentation** including PRD, ADRs, and guides

## Installation

### Prerequisites
- Python 3.10 or higher
- Ollama installed with llama3.2:3b model
- pip package manager

### Setup Steps

1. Clone or download the repository:
```bash
cd ~/LLM_HW3
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start Ollama in a separate terminal:
```bash
ollama serve
```

5. Verify setup:
```bash
python src/cli.py --help
```

## Usage

### Command 1: Single Translation

Translate a single sentence with optional error injection:

```bash
python src/cli.py translate "The quick brown fox jumps over the lazy dog" --error-rate 0.2
```

Parameters:
- `text`: The sentence to translate
- `--error-rate`: Error rate (0.0 to 0.5, default: 0.0)
- `--seed`: Random seed for reproducibility (default: 42)

### Command 2: Run Experiment

Execute a full experiment across multiple error rates:

```bash
python src/cli.py experiment
```

This will:
- Load test sentences from config/config.yaml
- Run translations for each error rate (0%, 10%, 20%, ..., 50%)
- Perform 3 runs per configuration for statistical validity
- Save results to results/experiment.json

### Command 3: Analyze Results

Generate visualizations and statistics from experiment results:

```bash
python src/cli.py analyze results/experiment.json
```

This will generate:
- error_impact_detailed.png (main results graph)
- distance_distributions.png (distribution histograms)
- distance_boxplot.png (box plot comparison)

## Project Structure

```
LLM_HW3/
├── src/
│   ├── agents/
│   │   ├── base_agent.py          # Abstract base class
│   │   ├── translator_agent.py    # Ollama-based translator
│   │   └── agent_chain.py         # Orchestration logic
│   ├── embeddings/
│   │   └── similarity.py          # Sentence embedding & distance
│   ├── utils/
│   │   └── error_injection.py     # Spelling error generation
│   └── cli.py                     # Command-line interface
├── tests/
│   ├── test_agents.py
│   ├── test_error_injection.py
│   └── test_embeddings.py
├── config/
│   └── config.yaml                # Experiment configuration
├── notebooks/
│   └── experiment_analysis.ipynb  # Data analysis & visualization
├── ADR/
│   ├── ADR-001-agent-architecture.md
│   ├── ADR-002-embedding-model.md
│   └── ADR-003-error-injection-strategy.md
├── results/
│   └── experiment.json            # Experiment output
├── README.md                      # This file
├── PRD.md                         # Product requirements
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git configuration
└── pytest.ini                     # Test configuration
```

## Configuration

Edit `config/config.yaml` to customize experiments:

```yaml
ollama:
  model: llama3.2:3b
  base_url: http://localhost:11434
  temperature: 0.3

experiment:
  error_rates: [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
  num_runs: 3
  seed: 42

test_sentences:
  - "Your test sentence here"
  - "Another sentence to test"
```

## Requirements

### System Requirements
- Python 3.10+
- RAM: 4GB minimum
- Ollama: Running locally on port 11434

### Python Dependencies
- typer (CLI framework)
- rich (terminal output)
- sentence-transformers (embeddings)
- transformers (NLP models)
- scipy (statistics)
- pandas (data processing)
- matplotlib (visualization)
- PyYAML (configuration)
- pytest (testing)

All dependencies are listed in `requirements.txt`

## Testing

Run the test suite:

```bash
pytest -v
```

Run with coverage report:

```bash
pytest --cov=src --cov-report=html
```

View coverage report:

```bash
open htmlcov/index.html
```

## Documentation

### Key Documents
- **PRD.md** - Product requirements and specifications
- **ADR/** - Architecture decision records
  - ADR-001: Multi-agent orchestration pattern
  - ADR-002: Embedding model selection
  - ADR-003: Error injection methodology
- **notebooks/experiment_analysis.ipynb** - Statistical analysis and insights

## Troubleshooting

### "Ollama not running"
```bash
ollama serve
```

### "Config file not found"
```bash
# Ensure you're running from project root
cd ~/LLM_HW3
```

### "Permission denied" on push
Create a Personal Access Token on GitHub and use it as password.

## Results Interpretation

The experiments measure how spelling errors affect semantic preservation across the translation chain:

- **Distance ≈ 0.0**: Perfect semantic preservation
- **Distance ≈ 0.1-0.3**: Good semantic preservation despite errors
- **Distance > 0.5**: Significant semantic drift

Linear analysis shows the relationship between error rate and semantic distance.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Author

Roie Gilad  
Email: roie@example.com  
Date: November 2025

## Citation

If you use this project in your research, please cite:

```bibtex
@software{gilad2025multilingual,
  title={Multi-Agent Translation Analysis System},
  author={Gilad, Roie},
  year={2025},
  url={https://github.com/roiegilad8/LLM_Agent_Orchestration_HW3}
}
```

## Acknowledgments

- Ollama for local LLM capabilities
- Hugging Face for Sentence Transformers
- The open-source community for excellent libraries