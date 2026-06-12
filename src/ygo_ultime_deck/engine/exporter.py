from typing import Dict, List
from pathlib import Path

def generate_ydk(decklist: Dict[str, List[int]], filepath: str | Path) -> None:
    """
    Génère un fichier .ydk standard à partir d'une decklist.
    
    Args:
        decklist: Un dictionnaire contenant 'main', 'extra' et 'side' avec des listes d'IDs de cartes.
        filepath: Le chemin complet où sauvegarder le fichier .ydk.
    """
    decklist = decklist or {}
    file_path = Path(filepath)
    
    # Créer le dossier s'il n'existe pas et s'il y a un dossier
    if file_path.parent and str(file_path.parent) != ".":
        file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("#created by YGO Ultime Deck\n")
        
        f.write("#main\n")
        for card_id in decklist.get("main", []):
            f.write(f"{card_id}\n")
            
        f.write("#extra\n")
        for card_id in decklist.get("extra", []):
            f.write(f"{card_id}\n")
            
        f.write("!side\n")
        for card_id in decklist.get("side", []):
            f.write(f"{card_id}\n")
