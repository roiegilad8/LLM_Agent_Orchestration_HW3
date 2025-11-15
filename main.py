"""CLI for running a multi-agent translation robustness experiment."""
from __future__ import annotations

import argparse
import json
import math
import random
import re
from collections import Counter
from dataclasses import asdict
from pathlib import Path
from typing import List, Sequence

from agents import DictionaryTranslationAgent


EN_FR_DICTIONARY = {
    "international": "internationale",
    "collaboration": "collaboration",
    "requires": "nécessite",
    "consistent": "cohérentes",
    "communication": "communication",
    "schedules": "horaires",
    "to": "pour",
    "support": "soutenir",
    "remote": "distants",
    "scientific": "scientifiques",
    "projects": "projets",
    "across": "atravers",
    "multiple": "multiples",
    "time": "fuseaux",
    "zones": "horaires",
    "and": "et",
    "languages": "langues",
    "careful": "soigneuse",
    "data": "données",
    "sharing": "partage",
    "ensures": "garantit",
    "teams": "équipes",
    "stay": "restent",
    "aligned": "alignées",
    "even": "même",
    "during": "pendant",
    "unexpected": "imprévus",
    "delays": "retards",
    "because": "car",
    "clear": "claires",
    "updates": "actualisations",
    "build": "construisent",
    "trust": "confiance",
    "between": "entre",
    "partners": "partenaires",
    "who": "qui",
    "rarely": "rarement",
    "meet": "rencontrent",
    "face": "face",
    "in": "en",
    "person": "personne",
    "regular": "régulières",
    "virtual": "virtuelles",
    "workshops": "ateliers",
    "also": "aussi",
    "help": "aident",
    "resolve": "résoudre",
    "technical": "techniques",
    "questions": "questions",
    "quickly": "rapidement",
    "so": "ainsi",
    "progress": "progrès",
    "continues": "continue",
    "steadily": "régulièrement",
}

FR_HE_DICTIONARY = {
    "internationale": "בינלאומית",
    "collaboration": "שיתוף_פעולה",
    "nécessite": "דורשת",
    "cohérentes": "עקביות",
    "communication": "תקשורת",
    "horaires": "לוחות",
    "pour": "כדי",
    "soutenir": "לתמוך",
    "distants": "מרוחקים",
    "scientifiques": "מדעיים",
    "projets": "פרויקטים",
    "atravers": "לאורך",
    "multiples": "מרובים",
    "fuseaux": "אזורים",
    "et": "ו",
    "langues": "שפות",
    "soigneuse": "קפדנית",
    "données": "נתונים",
    "partage": "שיתוף",
    "garantit": "מבטיח",
    "équipes": "צוותים",
    "restent": "נשארים",
    "alignées": "מתואמים",
    "même": "אפילו",
    "pendant": "במהלך",
    "imprévus": "בלתי_צפויים",
    "retards": "עיכובים",
    "car": "משום",
    "claires": "ברורות",
    "actualisations": "עדכונים",
    "construisent": "בונות",
    "confiance": "אמון",
    "entre": "בין",
    "partenaires": "שותפים",
    "qui": "ש",
    "rarement": "לעתים_רחוקות",
    "rencontrent": "נפגשים",
    "face": "פנים",
    "en": "ב",
    "personne": "אדם",
    "régulières": "סדירות",
    "virtuelles": "וירטואליות",
    "ateliers": "סדנאות",
    "aussi": "גם",
    "aident": "מסייעות",
    "résoudre": "לפתור",
    "techniques": "טכניים",
    "questions": "שאלות",
    "rapidement": "במהירות",
    "ainsi": "כך",
    "progrès": "התקדמות",
    "continue": "נמשכת",
    "régulièrement": "באופן_קבוע",
}

HE_EN_DICTIONARY = {
    "בינלאומית": "international",
    "שיתוף_פעולה": "collaboration",
    "דורשת": "requires",
    "עקביות": "consistent",
    "תקשורת": "communication",
    "לוחות": "schedules",
    "כדי": "to",
    "לתמוך": "support",
    "מרוחקים": "remote",
    "מדעיים": "scientific",
    "פרויקטים": "projects",
    "לאורך": "across",
    "מרובים": "multiple",
    "אזורים": "zones",
    "ו": "and",
    "שפות": "languages",
    "קפדנית": "careful",
    "נתונים": "data",
    "שיתוף": "sharing",
    "מבטיח": "ensures",
    "צוותים": "teams",
    "נשארים": "stay",
    "מתואמים": "aligned",
    "אפילו": "even",
    "במהלך": "during",
    "בלתי_צפויים": "unexpected",
    "עיכובים": "delays",
    "משום": "because",
    "ברורות": "clear",
    "עדכונים": "updates",
    "בונות": "build",
    "אמון": "trust",
    "בין": "between",
    "שותפים": "partners",
    "ש": "who",
    "לעתים_רחוקות": "rarely",
    "נפגשים": "meet",
    "פנים": "face",
    "ב": "in",
    "אדם": "person",
    "סדירות": "regular",
    "וירטואליות": "virtual",
    "סדנאות": "workshops",
    "גם": "also",
    "מסייעות": "help",
    "לפתור": "resolve",
    "טכניים": "technical",
    "שאלות": "questions",
    "במהירות": "quickly",
    "כך": "so",
    "התקדמות": "progress",
    "נמשכת": "continues",
    "באופן_קבוע": "steadily",
}

def build_agents() -> List[DictionaryTranslationAgent]:
    """Create the three-agent translation chain."""
    agent1 = DictionaryTranslationAgent(
        name="English→French Agent",
        source_language="English",
        target_language="French",
        dictionary=EN_FR_DICTIONARY,
        description="Word-level dictionary translator from English to French with fuzzy typo handling.",
    )
    agent2 = DictionaryTranslationAgent(
        name="French→Hebrew Agent",
        source_language="French",
        target_language="Hebrew",
        dictionary=FR_HE_DICTIONARY,
        description="Word-level dictionary translator from French to Hebrew with fuzzy typo handling.",
    )
    agent3 = DictionaryTranslationAgent(
        name="Hebrew→English Agent",
        source_language="Hebrew",
        target_language="English",
        dictionary=HE_EN_DICTIONARY,
        description="Word-level dictionary translator from Hebrew back to English with fuzzy typo handling.",
    )
    return [agent1, agent2, agent3]


def introduce_typos(sentence: str, error_rate: float, seed: int) -> str:
    """Introduce synthetic typos into a sentence based on the desired rate."""
    rng = random.Random(seed)
    tokens = sentence.split()
    word_indices = [i for i, token in enumerate(tokens) if any(ch.isalpha() for ch in token)]
    if not word_indices or error_rate <= 0:
        return sentence

    num_errors = max(1, math.ceil(len(word_indices) * error_rate))
    indices_to_modify = rng.sample(word_indices, k=min(num_errors, len(word_indices)))

    def corrupt(token: str) -> str:
        prefix = ""
        suffix = ""
        core = token
        while core and not core[0].isalnum():
            prefix += core[0]
            core = core[1:]
        while core and not core[-1].isalnum():
            suffix = core[-1] + suffix
            core = core[:-1]
        if not core:
            return token
        corrupted_core = _corrupt_word(core, rng)
        return prefix + corrupted_core + suffix

    for index in indices_to_modify:
        tokens[index] = corrupt(tokens[index])
    return " ".join(tokens)


def _corrupt_word(word: str, rng: random.Random) -> str:
    operations = ["substitute", "delete", "insert", "transpose"]
    operation = rng.choice(operations)
    chars = list(word)
    if operation == "substitute":
        position = rng.randrange(len(chars))
        chars[position] = rng.choice("abcdefghijklmnopqrstuvwxyz")
    elif operation == "delete" and len(chars) > 1:
        position = rng.randrange(len(chars))
        del chars[position]
    elif operation == "insert":
        position = rng.randrange(len(chars) + 1)
        chars.insert(position, rng.choice("abcdefghijklmnopqrstuvwxyz"))
    elif operation == "transpose" and len(chars) > 1:
        position = rng.randrange(len(chars) - 1)
        chars[position], chars[position + 1] = chars[position + 1], chars[position]
    else:  # fallback to substitution when delete/transpose not applicable
        position = rng.randrange(len(chars))
        chars[position] = rng.choice("abcdefghijklmnopqrstuvwxyz")
    return "".join(chars)


def run_pipeline(text: str, agents: Sequence[DictionaryTranslationAgent]) -> List[str]:
    outputs = [text]
    current = text
    for agent in agents:
        current = agent.translate(current)
        outputs.append(current)
    return outputs


def compute_distances(original: str, finals: Sequence[str]) -> List[float]:
    """Compute Euclidean distances using a simple TF-IDF embedding implementation."""
    corpus = [original, *finals]
    tokenized = [tokenize(text) for text in corpus]
    vocabulary = sorted({token for tokens in tokenized for token in tokens})
    if not vocabulary:
        return [0.0 for _ in finals]

    vocab_index = {term: idx for idx, term in enumerate(vocabulary)}
    document_count = len(corpus)
    doc_freq = Counter()
    for tokens in tokenized:
        doc_freq.update(set(tokens))

    idf = {
        term: math.log((1 + document_count) / (1 + doc_freq[term])) + 1.0
        for term in vocabulary
    }

    vectors: List[List[float]] = []
    for tokens in tokenized:
        counts = Counter(tokens)
        length = max(len(tokens), 1)
        vector = [0.0] * len(vocabulary)
        for term, count in counts.items():
            idx = vocab_index[term]
            tf = count / length
            vector[idx] = tf * idf[term]
        vectors.append(vector)

    original_vec = vectors[0]
    distances = [euclidean_distance(original_vec, vectors[i]) for i in range(1, len(vectors))]
    return distances


def count_words(text: str) -> int:
    return sum(1 for token in text.split() if any(ch.isalpha() for ch in token))


def save_json(data, path: Path) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def tokenize(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z_]+", text.lower())


def euclidean_distance(vec1: Sequence[float], vec2: Sequence[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(vec1, vec2)))


def plot_results(error_rates: Sequence[float], distances: Sequence[float], output_path: Path) -> None:
    width, height = 800, 500
    margin = 60
    max_rate = max(error_rates) if error_rates else 1.0
    max_rate = max(max_rate, 1e-6)
    max_distance = max(distances) if distances else 1.0
    max_distance = max(max_distance, 1e-6)

    def scale_x(rate: float) -> float:
        return margin + (width - 2 * margin) * (rate / max_rate)

    def scale_y(distance: float) -> float:
        return height - margin - (height - 2 * margin) * (distance / max_distance)

    points = [(scale_x(rate), scale_y(distance)) for rate, distance in zip(error_rates, distances)]

    markers = "".join(
        f'<circle cx="{x:.2f}" cy="{y:.2f}" r="5" fill="#1f77b4" />'
        for x, y in points
    )

    rate_labels = "".join(
        f'<text x="{scale_x(rate):.2f}" y="{height - margin + 25}" text-anchor="middle" font-size="14">{rate:.2f}</text>'
        for rate in error_rates
    )

    svg_content = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="white" />
  <line x1="{margin}" y1="{height - margin}" x2="{width - margin}" y2="{height - margin}" stroke="black" stroke-width="2" />
  <line x1="{margin}" y1="{height - margin}" x2="{margin}" y2="{margin}" stroke="black" stroke-width="2" />
  <text x="{width / 2}" y="{height - 10}" text-anchor="middle" font-size="16">Spelling error rate</text>
  <text transform="translate(20 {height / 2}) rotate(-90)" text-anchor="middle" font-size="16">Vector distance (Euclidean)</text>
  <polyline fill="none" stroke="#1f77b4" stroke-width="3" points="{' '.join(f'{x:.2f},{y:.2f}' for x, y in points)}" />
  {markers}
  {rate_labels}
  <text x="{width / 2}" y="{margin - 20}" text-anchor="middle" font-size="18" font-weight="bold">Effect of Spelling Errors on Translation Consistency</text>
</svg>
"""

    output_path.write_text(svg_content.strip() + "\n")


DEFAULT_SENTENCE = (
    "International collaboration requires consistent communication schedules to support remote scientific "
    "projects across multiple time zones and languages. Careful data sharing ensures teams stay aligned even "
    "during unexpected delays because clear updates build trust between partners who rarely meet face to face in "
    "person. Regular virtual workshops also help resolve technical questions quickly so progress continues steadily."
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the multi-agent translation typo robustness experiment.")
    parser.add_argument(
        "--sentence",
        type=str,
        default=DEFAULT_SENTENCE,
        help="Base English sentence to use for the experiment (≥15 words).",
    )
    parser.add_argument(
        "--error-rates",
        type=float,
        nargs="*",
        default=[0.0, 0.15, 0.25, 0.35, 0.45, 0.5],
        help="List of spelling error rates to evaluate (between 0 and 0.5).",
    )
    parser.add_argument(
        "--seed", type=int, default=42, help="Random seed for reproducible typo generation."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results"),
        help="Directory where experiment artifacts will be saved.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    agents = build_agents()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    runs = []
    final_sentences = []

    for idx, rate in enumerate(args.error_rates):
        corrupted = introduce_typos(args.sentence, rate, seed=args.seed + idx)
        pipeline_outputs = run_pipeline(corrupted, agents)
        final_sentence = pipeline_outputs[-1]
        final_sentences.append(final_sentence)
        runs.append(
            {
                "error_rate": rate,
                "input_sentence": corrupted,
                "french_translation": pipeline_outputs[1],
                "hebrew_translation": pipeline_outputs[2],
                "final_sentence": final_sentence,
                "input_length": count_words(corrupted),
                "final_length": count_words(final_sentence),
            }
        )

    distances = compute_distances(args.sentence, final_sentences)
    for run, distance in zip(runs, distances):
        run["distance"] = distance

    plot_path = args.output_dir / "spelling_error_distance.svg"
    plot_results(args.error_rates, distances, plot_path)

    report = {
        "base_sentence": args.sentence,
        "base_length": count_words(args.sentence),
        "agents": [asdict(agent.describe()) for agent in agents],
        "runs": runs,
        "plot_path": str(plot_path),
    }

    save_json(report, args.output_dir / "experiment_report.json")

    sentences_log = "\n\n".join(
        [
            "Base sentence:\n" + args.sentence,
            *[
                f"Error rate {run['error_rate']:.2f} input:\n{run['input_sentence']}\nFinal output:\n{run['final_sentence']}"
                for run in runs
            ],
        ]
    )
    (args.output_dir / "sentences.txt").write_text(sentences_log + "\n")

    print("Experiment completed. Report saved to", args.output_dir)
    print("Vector distances:")
    for run in runs:
        print(f"  error_rate={run['error_rate']:.2f} -> distance={run['distance']:.4f}")


if __name__ == "__main__":
    main()
