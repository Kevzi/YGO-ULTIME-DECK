import typer
from rich.console import Console

app = typer.Typer(help="Moteur d'optimisation de deck Yu-Gi-Oh! (YGO ULTIME DECK)", rich_markup_mode="rich")
console = Console()

@app.callback()
def main():
    """
    [bold green]YGO ULTIME DECK[/bold green] - Moteur mathématique et analytique pour Yu-Gi-Oh!
    """
    pass

if __name__ == "__main__":
    app()
