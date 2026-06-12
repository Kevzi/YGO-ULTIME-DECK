import yaml
import typer
from pathlib import Path
from pydantic import ValidationError
from rich.console import Console

from ygo_ultime_deck.models.meta import MetaTargetsRequest

console = Console(stderr=True)

DEFAULT_META_CONTENT = """# Fichier de configuration des menaces Méta (meta_targets.yaml)
# Définissez ici les staples ou interruptions adverses.
threats:
  - name: "Ash Blossom & Joyous Spring"
    category: "Handtrap"
    count: 3
  - name: "Infinite Impermanence"
    category: "Handtrap"
    count: 3
  - name: "Nibiru, the Primal Being"
    category: "Handtrap"
    count: 1
"""

def load_meta_targets(filepath: Path | str) -> MetaTargetsRequest:
    """
    Load meta targets from a YAML file.
    Creates a default configuration file if it doesn't exist.
    
    Args:
        filepath: Path to the YAML file.
        
    Returns:
        A validated MetaTargetsRequest object.
        
    Raises:
        typer.Exit(1): If the file is invalid YAML, violates schema, or cannot be read.
    """
    path = Path(filepath)
    
    if not path.exists():
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(DEFAULT_META_CONTENT, encoding="utf-8")
            data = yaml.safe_load(DEFAULT_META_CONTENT)
            return MetaTargetsRequest(**data)
        except PermissionError:
            console.print(f"[bold red]Erreur critique : Permission refusée pour créer le fichier {path}.[/bold red]")
            raise typer.Exit(code=1)
        except OSError as e:
            console.print(f"[bold red]Erreur critique lors de la création du fichier {path} :[/bold red]\n{e}")
            raise typer.Exit(code=1)
        
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            
        if data is None:
            console.print(f"[bold red]Erreur critique : Le fichier {path} est vide.[/bold red]")
            raise typer.Exit(code=1)
            
        if isinstance(data, list):
            data = {"threats": data}
            
        if not isinstance(data, dict):
            console.print(f"[bold red]Erreur critique : Le fichier {path} a un format invalide (doit être une liste ou un dictionnaire).[/bold red]")
            raise typer.Exit(code=1)
            
        return MetaTargetsRequest(**data)
        
    except PermissionError:
        console.print(f"[bold red]Erreur critique : Permission refusée pour lire le fichier {path}.[/bold red]")
        raise typer.Exit(code=1)
    except OSError as e:
        console.print(f"[bold red]Erreur d'accès ou de lecture du fichier {path} :[/bold red]\n{e}")
        raise typer.Exit(code=1)
    except UnicodeDecodeError as e:
        console.print(f"[bold red]Erreur d'encodage (doit être UTF-8) dans {path} :[/bold red]\n{e}")
        raise typer.Exit(code=1)
    except yaml.YAMLError as e:
        console.print(f"[bold red]Erreur critique lors de l'analyse du fichier YAML {path} :[/bold red]\n{e}")
        raise typer.Exit(code=1)
    except ValidationError as e:
        console.print(f"[bold red]Erreur de validation de schéma dans {path} :[/bold red]\n{e}")
        raise typer.Exit(code=1)
