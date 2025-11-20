# Multi-Agent Translation Robustness Experiment

This repository contains a command-line workflow that simulates a three-agent translation
pipeline and measures how spelling errors influence the fidelity of the round-trip
translation. The pipeline translates an English sentence to French, then to Hebrew, and
finally back to English. Each agent is implemented as a dictionary-backed translator with
basic fuzzy matching so that it can handle noisy tokens.

Running the CLI generates:

- The original English sentence (at least 56 words in the default example).
- Noisy inputs for multiple spelling error rates (0%–50%).
- Intermediate French and Hebrew translations for every run.
- Final English sentences after the round trip.
- A JSON report that records sentence lengths, agent descriptions, and Euclidean distances
  between the original and final embeddings.
- A simple SVG line chart illustrating how the vector distance grows with higher typo
  rates.

All experiment artifacts are written to the `results/` directory.

## Prerequisites

The project uses only the Python standard library. No external packages are required.

## Usage

```bash
python main.py --output-dir results
```

Optional flags:

- `--sentence` – Provide a custom English sentence (≥15 words) to translate.
- `--error-rates` – Specify the spelling error percentages to test (default: `0.0 0.15 0.25 0.35 0.45 0.5`).
- `--seed` – Control the randomness of the synthetic typos.

After execution, inspect the generated files:

- `results/experiment_report.json` – Complete run metadata, including agent descriptions, word counts, typoed sentences, intermediate translations, and distances.
- `results/sentences.txt` – Human-readable list of the base sentence and every noisy input/final output pair.
- `results/spelling_error_distance.svg` – Line chart comparing error rates and embedding distances.

## Experiment Summary

Using the default sentence and typo rates, the Euclidean distances (derived from a custom
TF-IDF embedding) between the original and round-trip translations were:

| Error rate | Distance |
|-----------:|---------:|
| 0.00       | 0.0462   |
| 0.15       | 0.0462   |
| 0.25       | 0.0462   |
| 0.35       | 0.0660   |
| 0.45       | 0.0660   |
| 0.50       | 0.1018   |

The results show that the handcrafted translation chain remains stable until high typo
levels begin to alter multiple tokens, at which point the round-trip output deviates more
strongly from the original sentence.
