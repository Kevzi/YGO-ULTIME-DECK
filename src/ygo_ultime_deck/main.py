"""Main CLI entry point for YGO ULTIME DECK."""

import sys
import asyncio
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

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

@app.command()
def audit(
    iterations: int = typer.Option(100000, "--iterations", "-i", help="Nombre d'itérations de simulation"),
    hand_size: int = typer.Option(5, "--hand-size", "-h", help="Taille de la main"),
    workers: Optional[int] = typer.Option(None, "--workers", "-w", help="Workers multiprocessing"),
    starters: int = typer.Option(12, "--starters", "-s", help="Nombre de Starters"),
    garnets: int = typer.Option(2, "--garnets", "-g", help="Nombre de Garnets"),
    core: int = typer.Option(25, "--core", "-c", help="Taille du Core Engine"),
    output: Path = typer.Option(Path("output/decklist_ultime.ydk"), "--output", "-o", help="Chemin d'export du .ydk")
):
    """
    Exécute l'audit complet : Optimisation de taille, Simulation (Immunités), et Export YDK.
    """
    from ygo_ultime_deck.engine.config_parser import parse_target_combos
    from ygo_ultime_deck.engine.monte_carlo import run_monte_carlo_simulation
    from ygo_ultime_deck.engine.optimizer import optimize_deck_size
    from ygo_ultime_deck.engine.exporter import generate_ydk
    from ygo_ultime_deck.engine.resolver import CardResolver
    import logging
    
    logger = logging.getLogger(__name__)
    
    console.print(Panel.fit("[bold magenta]AUDIT DECK ULTIME[/bold magenta]", border_style="magenta"))
    
    # 1. Optimisation de la taille du deck
    try:
        opt_result = optimize_deck_size(starters, garnets, core)
        opt_size = opt_result["optimal_size"]
        p_starter = opt_result["metrics"]["p_starter"] * 100
        p_garnet = (1.0 - opt_result["metrics"]["p_no_garnet"]) * 100
    except ValueError as e:
        console.print(f"[bold red]Erreur Optimiseur :[/bold red] {e}")
        raise typer.Exit(1)
        
    # 2. Simulation Monte-Carlo
    config_path = Path(__file__).resolve().parent.parent.parent / "config" / "target_combos.yaml"
    try:
        request = parse_target_combos(config_path)
    except Exception as e:
        console.print(f"[bold yellow]Avertissement (Config) :[/bold yellow] Impossible de charger target_combos.yaml : {e}")
        request = None
        
    sim_result = None
    if request:
        # Deck mock pour la simulation basé sur l'optimiseur
        # On respecte le core (si renseigné) et on ne dépasse pas la taille
        num_bricks = max(0, opt_size - starters - garnets - core)
        deck = ["Starter"] * starters + ["Garnet"] * garnets + ["Extender"] * core + ["Brick"] * num_bricks
        
        # S'assurer qu'on ne dépasse pas la taille stricte (les bricks seront tronquées si la somme > opt_size)
        deck = deck[:opt_size]
        
        try:
            sim_result = asyncio.run(run_monte_carlo_simulation(deck, request, hand_size, iterations, workers))
        except Exception as e:
            console.print(f"[bold red]Erreur Simulation :[/bold red] {e}")
    
    # 3. Export YDK
    # Récupération des vrais noms depuis target_combos.yaml si disponibles
    export_names = []
    if request and request.combos:
        for combo in request.combos:
            if not combo.requirements:
                continue
            for req in combo.requirements:
                # Ajoute chaque carte selon son nombre d'exemplaires requis (max 3 par convention, ou opt_size)
                count = int(req.count) if isinstance(req.count, (int, str)) and str(req.count).isdigit() else 1
                for _ in range(count):
                    export_names.append(req.name)
                    
    # Compléter avec des cartes génériques si on n'atteint pas opt_size
    remaining = max(0, opt_size - len(export_names))
    if remaining > 0:
        export_names.extend(["Generic Card"] * remaining)
        
    # Tronquer si on dépasse la taille opt_size
    if len(export_names) > opt_size:
        logger.warning(f"La configuration demande plus de cartes ({len(export_names)}) que la taille optimale ({opt_size}). Troncature silencieuse.")
        export_names = export_names[:opt_size]
    
    # Résolution des IDs (Seulement si l'exportation est nécessaire, on le fait juste avant de générer le YDK)
    cache_path = Path(__file__).resolve().parent.parent.parent / "data" / "cache" / "aggregate.zip"
    resolver = CardResolver(cache_path)
    resolved_ids = resolver.resolve(export_names)
    
    decklist = {
        "main": resolved_ids,
        "extra": [],
        "side": []
    }
    export_success = False
    try:
        generate_ydk(decklist, output)
        export_success = True
    except Exception as e:
        console.print(f"[bold red]Erreur Export :[/bold red] {e}")
        
    # 4. Affichage du Rapport Rich
    table = Table(title="Rapport d'Audit Yu-Gi-Oh!", box=box.ROUNDED)
    table.add_column("Métrique", style="cyan", no_wrap=True)
    table.add_column("Valeur", justify="right", style="green")
    
    table.add_row("Taille de Deck Optimale", f"{opt_size} cartes")
    table.add_row("Consistance (Starter >= 1)", f"{p_starter:.2f}%")
    table.add_row("Risque de Brick (Garnet >= 1)", f"{p_garnet:.2f}%")
    
    if sim_result and sim_result.total_iterations > 0:
        for combo_name, successes in sim_result.combo_success_rates.items():
            rate = (successes / sim_result.total_iterations) * 100
            table.add_row(f"Combo: {combo_name}", f"{rate:.2f}%")
            
            # Immunity stats
            if combo_name in sim_result.immunity_success_rates:
                for threat, imm_succ in sim_result.immunity_success_rates[combo_name].items():
                    # Immunity is calculated over the successful hands
                    if successes > 0:
                        imm_rate = (imm_succ / successes) * 100
                        table.add_row(f" └─ Immunité vs {threat}", f"{imm_rate:.2f}%")
                        
    console.print(table)
    if export_success:
        console.print(f"[italic dim]Decklist exportée vers: {output}[/italic dim]")

if __name__ == "__main__":
    app()
