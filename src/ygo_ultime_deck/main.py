"""Main CLI entry point for YGO ULTIME DECK."""

import sys
import asyncio
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

app = typer.Typer(help="Moteur d'optimisation de deck Yu-Gi-Oh! (YGO ULTIME DECK)", rich_markup_mode="rich")
console = Console()

def global_exception_handler(exc_type, exc_value, exc_traceback):
    """Handle unhandled exceptions globally, formatting with Rich."""
    if issubclass(exc_type, typer.Exit):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    console.print(f"[bold red]Erreur inattendue :[/bold red] {exc_value}")
    sys.exit(1)

sys.excepthook = global_exception_handler


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    update: bool = typer.Option(False, "--update", help="Télécharger et mettre à jour le cache YGOJSON"),
):
    """
    [bold green]YGO ULTIME DECK[/bold green] - Moteur mathématique et analytique pour Yu-Gi-Oh!
    """
    if update:
        import httpx
        from ygo_ultime_deck.ingestion.downloader import download_ygojson

        target_path = Path(__file__).resolve().parent.parent.parent / "data" / "cache" / "aggregate.zip"
        try:
            asyncio.run(download_ygojson(target_path=target_path))
            console.print("[bold green]Téléchargement terminé avec succès ![/bold green]")
        except httpx.HTTPError as e:
            console.print(f"[bold red]Erreur réseau lors du téléchargement :[/bold red] {e}")
            raise typer.Exit(1)
        except Exception as e:
            console.print(f"[bold red]Erreur inattendue :[/bold red] {e}")
            raise typer.Exit(1)
            
    elif ctx.invoked_subcommand is None:
        console.print(ctx.get_help())

@app.command()
def simulate(
    iterations: int = typer.Option(100000, "--iterations", "-i", help="Nombre d'itérations de simulation"),
    hand_size: int = typer.Option(5, "--hand-size", "-h", help="Taille de la main de départ"),
    workers: Optional[int] = typer.Option(None, "--workers", "-w", help="Nombre de processus à utiliser")
):
    """
    Simule la probabilité de réussite des combos cibles via Monte-Carlo.
    """
    from ygo_ultime_deck.engine.config_parser import parse_target_combos
    from ygo_ultime_deck.engine.monte_carlo import run_monte_carlo_simulation
    
    config_path = Path(__file__).resolve().parent.parent.parent / "config" / "target_combos.yaml"
    
    # Parser les combos depuis le fichier config
    try:
        request = parse_target_combos(config_path)
    except Exception as e:
        console.print(f"[bold red]Erreur de lecture des combos :[/bold red] {e}")
        raise typer.Exit(1)

    # Pour l'instant (Epic 3.3), le YDK n'est pas parsé, on mock un deck basique
    # On simule un deck de 40 cartes avec 5 Starters et 3 Extenders
    deck = ["Starter"] * 5 + ["Extender"] * 3 + ["Garnet"] * 32
    
    console.print(f"[bold blue]Démarrage de la simulation Monte-Carlo ({iterations} itérations)[/bold blue]")
    
    try:
        result = asyncio.run(run_monte_carlo_simulation(deck, request, hand_size, iterations, workers))
    except ValueError as e:
        console.print(f"[bold red]Erreur de validation :[/bold red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]Erreur lors de la simulation :[/bold red] {e}")
        raise typer.Exit(1)
    
    console.print("[bold green]Simulation terminée ![/bold green]\n")
    console.print("[bold]Résultats :[/bold]")
    for combo_name, successes in result.combo_success_rates.items():
        rate = (successes / result.total_iterations) * 100
        console.print(f" - {combo_name} : {rate:.2f}% ({successes}/{result.total_iterations})")

if __name__ == "__main__":
    app()
