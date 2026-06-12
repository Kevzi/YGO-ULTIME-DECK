"""YGOJSON parser module."""

import json
import zipfile
from pathlib import Path
from typing import List

from pydantic import ValidationError

from ygo_ultime_deck.models.card import CardModel


def load_and_parse_ygojson(zip_path: Path) -> List[CardModel]:
    """
    Load YGOJSON data from a zip file and parse it into a list of CardModels.
    
    Args:
        zip_path: Path to the aggregate.zip file.
        
    Returns:
        List of CardModels that are valid TCG/OCG cards.
    """
    valid_cards = []
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            json_filename = next((name for name in zf.namelist() if name.endswith('.json')), None)
            
            if not json_filename:
                raise FileNotFoundError("No JSON file found in the provided zip archive.")
                
            with zf.open(json_filename) as f:
                data = json.load(f)
                
                # Handling both array of cards and dict with data key
                cards_list = data.get("data", []) if isinstance(data, dict) else data
                
                # If data was a dict but we couldn't find 'data' key or it's not a list
                if not isinstance(cards_list, list):
                    return []
                
                for card_data in cards_list:
                    if not isinstance(card_data, dict):
                        continue
                        
                    # Filtrage des formats (TCG ou OCG doivent être présents)
                    formats = card_data.get("formats", [])
                    if not isinstance(formats, list):
                        continue
                        
                    if "TCG" not in formats and "OCG" not in formats:
                        continue
                        
                    # Filtrage de la Banlist (Ignorer les cartes illégales)
                    banlist_info = card_data.get("banlist_info", {})
                    if isinstance(banlist_info, dict) and ("Banned" in banlist_info.values()):
                        continue
                        
                    # Exclusion des Tokens
                    card_type = card_data.get("type", "")
                    if card_type == "Token":
                        continue
                        
                    try:
                        card_model = CardModel(**card_data)
                        valid_cards.append(card_model)
                    except (ValidationError, KeyError):
                        # Swallow instantiation errors to ensure resilience
                        pass
                        
    except (zipfile.BadZipFile, json.JSONDecodeError):
        # Graceful degradation if the cache file is completely corrupted
        pass
        
    return valid_cards
