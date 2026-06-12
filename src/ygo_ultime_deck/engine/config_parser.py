import yaml
import typer
import os
from pathlib import Path
from rich.console import Console
from pydantic import ValidationError
from ygo_ultime_deck.models.simulation import SimulationRequest

console = Console()

def parse_target_combos(file_path: str) -> SimulationRequest:
    path_obj = Path(file_path)
    
    # Path constraint: must be in config/
    try:
        # Resolve to absolute path to ensure no traversal tricks bypass the check
        abs_target = path_obj.resolve(strict=False)
        abs_config = Path("config").resolve(strict=False)
        
        if abs_config not in abs_target.parents and abs_target.parent != abs_config:
            console.print(f"[bold red]Erreur critique :[/bold red] Le fichier '{file_path}' doit résider dans le répertoire 'config/'.")
            raise typer.Exit(1)
    except Exception:
        pass

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            
        if not data:
            console.print(f"[bold red]Erreur critique :[/bold red] Le fichier '{file_path}' est vide ou ne contient aucune donnée YAML valide.")
            raise typer.Exit(1)
            
        if not isinstance(data, dict):
            console.print(f"[bold red]Erreur critique :[/bold red] Le format racine du fichier '{file_path}' doit être un dictionnaire (clé-valeur), et non une liste ou une valeur simple.")
            raise typer.Exit(1)
            
        return SimulationRequest(**data)
        
    except FileNotFoundError:
        console.print(f"[bold red]Erreur critique :[/bold red] Le fichier '{file_path}' est introuvable.")
        raise typer.Exit(1)
    except IsADirectoryError:
        console.print(f"[bold red]Erreur critique :[/bold red] '{file_path}' est un répertoire, pas un fichier.")
        raise typer.Exit(1)
    except PermissionError:
        console.print(f"[bold red]Erreur critique :[/bold red] Permission refusée pour lire '{file_path}'.")
        raise typer.Exit(1)
    except UnicodeDecodeError:
        console.print(f"[bold red]Erreur critique :[/bold red] Le fichier '{file_path}' n'est pas encodé en UTF-8.")
        raise typer.Exit(1)
    except yaml.YAMLError as e:
        console.print(f"[bold red]Erreur critique :[/bold red] Le fichier YAML '{file_path}' est malformé.\n{e}")
        raise typer.Exit(1)
    except ValidationError as e:
        console.print(f"[bold red]Erreur critique :[/bold red] Le contenu du fichier '{file_path}' ne respecte pas le schéma attendu.\n{e}")
        raise typer.Exit(1)
