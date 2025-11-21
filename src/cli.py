"""Command-line interface for the translation system."""
import logging
import json
import sys
from pathlib import Path
import typer
from rich.console import Console
from rich.progress import track, Progress, SpinnerColumn, TextColumn
import yaml

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from agents.agent_chain import TranslationChain
from embeddings.similarity import SimilarityCalculator
from utils.error_injection import inject_errors

app = typer.Typer()
console = Console()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


@app.command()
def translate(
    text: str = typer.Argument(..., help="Text to translate"),
    error_rate: float = typer.Option(0.0, min=0.0, max=0.5, help="Error rate"),
    seed: int = typer.Option(42, help="Random seed"),
):
    """Run single translation chain."""
    console.print(f"[bold]Original:[/bold] {text}")
    
    if error_rate > 0:
        text_corrupted = inject_errors(text, error_rate, seed)
        console.print(f"[yellow]Corrupted:[/yellow] {text_corrupted}")
    else:
        text_corrupted = text
    
    chain = TranslationChain()
    result = chain.run(text_corrupted)
    
    console.print(f"[bold green]Final:[/bold green] {result['final']}")
    
    calc = SimilarityCalculator()
    distance = calc.calculate_distance(text, result['final'])
    console.print(f"[cyan]Semantic Distance:[/cyan] {distance:.4f}")


@app.command()
def experiment(
    config_path: Path = typer.Option("config/config.yaml", help="Config file"),
    output: Path = typer.Option("results/experiment.json", help="Output file"),
):
    """Run full experiment across error rates."""
    if not config_path.exists():
        console.print(f"[red]Config not found: {config_path}[/red]")
        raise typer.Exit(1)
    
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    sentences = config['test_sentences']
    error_rates = config['experiment']['error_rates']
    num_runs = config['experiment']['num_runs']
    seed = config['experiment']['seed']
    
    chain = TranslationChain()
    calc = SimilarityCalculator()
    
    results = []
    total = len(sentences) * len(error_rates) * num_runs
    console.print(f"[bold]Running {total} translations...[/bold]")
    
    with Progress() as progress:
        task = progress.add_task("Experiment...", total=total)
        
        for sentence_idx, sentence in enumerate(sentences):
            for error_rate in error_rates:
                for run in range(num_runs):
                    corrupted = inject_errors(sentence, error_rate, seed + run)
                    translation = chain.run(corrupted)
                    distance = calc.calculate_distance(sentence, translation['final'])
                    
                    results.append({
                        "sentence_id": sentence_idx,
                        "original": sentence,
                        "error_rate": error_rate,
                        "run": run,
                        "corrupted": corrupted,
                        "final": translation['final'],
                        "distance": float(distance)
                    })
                    
                    progress.update(task, advance=1)
    
    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    console.print(f"[green]✓[/green] Results saved to {output}")


@app.command()
def analyze(
    input_file: Path = typer.Argument(..., help="Experiment JSON"),
    output: Path = typer.Option("results/error_impact_graph.png", help="Graph output"),
):
    """Generate graph from results."""
    import pandas as pd
    import matplotlib.pyplot as plt
    
    if not input_file.exists():
        console.print(f"[red]File not found: {input_file}[/red]")
        raise typer.Exit(1)
    
    with open(input_file, encoding='utf-8') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    grouped = df.groupby(['error_rate', 'sentence_id'])['distance'].agg(['mean', 'std']).reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 7))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    for i, sid in enumerate(sorted(grouped['sentence_id'].unique())):
        subset = grouped[grouped['sentence_id'] == sid].sort_values('error_rate')
        
        ax.plot(
            subset['error_rate'] * 100,
            subset['mean'],
            marker='o',
            label=f'Sentence {sid + 1}',
            linewidth=2.5,
            markersize=8,
            color=colors[i % len(colors)]
        )
        
        if (subset['std'] > 0).any():
            ax.fill_between(
                subset['error_rate'] * 100,
                subset['mean'] - subset['std'],
                subset['mean'] + subset['std'],
                alpha=0.2,
                color=colors[i % len(colors)]
            )
    
    ax.set_xlabel('Spelling Error Rate (%)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Cosine Distance', fontsize=13, fontweight='bold')
    ax.set_title('Impact of Spelling Errors on Semantic Preservation', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output, dpi=300, bbox_inches='tight')
    console.print(f"[green]✓[/green] Graph saved to {output}")
    plt.close()


if __name__ == "__main__":
    app()
