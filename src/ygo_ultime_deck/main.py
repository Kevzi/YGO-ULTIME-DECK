import sys
import typer
from rich.console import Console

app = typer.Typer(help="Moteur d'optimisation de deck Yu-Gi-Oh! (YGO ULTIME DECK)", rich_markup_mode="rich")
console = Console()

def global_exception_handler(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, typer.Exit):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    console.print(f"[bold red]Erreur inattendue :[/bold red] {exc_value}")
    sys.exit(1)

sys.excepthook = global_exception_handler

@app.callback()
def main():
    """
    [bold green]YGO ULTIME DECK[/bold green] - Moteur mathématique et analytique pour Yu-Gi-Oh!
    """
    pass

if __name__ == "__main__":
    app()
