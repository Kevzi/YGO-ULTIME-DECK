import yaml
import typer
from pathlib import Path
from rich.console import Console

console = Console(stderr=True)

DEFAULT_CONFIG_CONTENT = """# Fichier de configuration des règles de tags (tags_rules.yaml)
# Définissez ici les Regex pour catégoriser vos cartes.
# Les clés sont les noms des tags, les valeurs sont les Regex correspondantes.
#
# NOTE : La sensibilité à la casse est respectée par défaut.
# Si vous souhaitez qu'une règle ignore la casse, commencez-la par `(?i)`.
# Exemple : `(?i)add .* from your deck to your hand`

Starter: '(?i)Normal Summon.*add.*from your Deck to your hand'
Extender: '(?i)Special Summon this card'
HandTrap: '(?i)Discard this card.*negate that effect'
BoardBreaker: '(?i)destroy all monsters your opponent controls'
"""

def load_tags_rules(filepath: Path | str) -> dict[str, str]:
    """
    Load tags rules from a YAML file.
    Creates a default configuration file if it doesn't exist.
    
    Args:
        filepath: Path to the YAML file.
        
    Returns:
        A dictionary mapping tags to regex patterns.
        
    Raises:
        typer.Exit(1): If the file is invalid YAML or cannot be read.
    """
    path = Path(filepath)
    
    if not path.exists():
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(DEFAULT_CONFIG_CONTENT, encoding="utf-8")
        except PermissionError:
            console.print(f"[bold red]Erreur critique : Permission refusée pour créer le fichier {path}.[/bold red]")
            raise typer.Exit(code=1)
        except OSError as e:
            console.print(f"[bold red]Erreur critique lors de la création du fichier {path} :[/bold red]\n{e}")
            raise typer.Exit(code=1)
        
    try:
        with open(path, "r", encoding="utf-8") as f:
            rules = yaml.safe_load(f)
            
        if rules is None:
            console.print(f"[bold red]Erreur critique : Le fichier {path} est vide.[/bold red]")
            raise typer.Exit(code=1)
            
        if not isinstance(rules, dict):
            console.print(f"[bold red]Erreur critique : Le fichier {path} doit contenir un dictionnaire (clé-valeur).[/bold red]")
            raise typer.Exit(code=1)
            
        # Ensure all keys and values are strings
        for k, v in rules.items():
            if not isinstance(k, str) or not isinstance(v, str):
                console.print(f"[bold red]Erreur critique : Dans le fichier {path}, toutes les clés et valeurs doivent être des chaînes de caractères.[/bold red]")
                raise typer.Exit(code=1)
                
        return rules
        
    except PermissionError:
        console.print(f"[bold red]Erreur critique : Permission refusée pour lire le fichier {path}.[/bold red]")
        raise typer.Exit(code=1)
    except yaml.YAMLError as e:
        console.print(f"[bold red]Erreur critique lors de l'analyse du fichier YAML {path} :[/bold red]\n{e}")
        raise typer.Exit(code=1)

