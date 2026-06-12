"""Main CLI entry point for YGO ULTIME DECK."""

import sys
import asyncio
from pathlib import Path

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

if __name__ == "__main__":
    app()
