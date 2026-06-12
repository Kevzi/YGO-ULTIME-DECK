"""Module de résolution de noms en IDs."""
import json
import zipfile
import logging
import io
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

DEFAULT_MOCK_ID = 11111111

class CardResolver:
    """Résout les noms de cartes en IDs officiels via le cache YGOJSON."""
    
    def __init__(self, cache_path: Path):
        self.cache_path = cache_path
        self._name_to_id: Dict[str, int] = {}
        self._loaded = False
        
    def _load_database(self) -> None:
        """Charge la base de données paresseusement."""
        if self._loaded:
            return
            
        if not self.cache_path.exists():
            logger.warning(f"Fichier de cache introuvable : {self.cache_path}. La résolution d'IDs utilisera des mocks.")
            self._loaded = True
            return
            
        try:
            with zipfile.ZipFile(self.cache_path, 'r') as zf:
                json_filename = next((name for name in zf.namelist() if name.endswith('.json')), None)
                if not json_filename:
                    logger.warning("Aucun fichier JSON dans l'archive. Utilisation de mocks.")
                    self._loaded = True
                    return
                    
                with zf.open(json_filename) as f:
                    with io.TextIOWrapper(f, encoding='utf-8') as text_f:
                        data = json.load(text_f)
                        cards_list = data.get("data", []) if isinstance(data, dict) else data
                        
                        if not isinstance(cards_list, list):
                            self._loaded = True
                            return
                            
                        for card_data in cards_list:
                            if not isinstance(card_data, dict):
                                continue
                                
                            card_name = card_data.get("name")
                            card_id = card_data.get("id")
                            
                            if card_name and card_id is not None:
                                try:
                                    self._name_to_id[str(card_name).strip().lower()] = int(card_id)
                                except (ValueError, TypeError):
                                    pass
                            
        except (zipfile.BadZipFile, json.JSONDecodeError, OSError) as e:
            logger.warning(f"Erreur lors de la lecture du cache YGOJSON : {e}")
            
        self._loaded = True

    def resolve(self, names: Optional[List[str]]) -> List[int]:
        """
        Résout une liste de noms de cartes en liste d'IDs.
        Retourne DEFAULT_MOCK_ID par défaut si introuvable.
        """
        if not names:
            return []
            
        if isinstance(names, str):
            names = [names]
            
        self._load_database()
        
        ids = []
        for name in names:
            if not name:
                ids.append(DEFAULT_MOCK_ID)
                continue
                
            resolved_id = self._name_to_id.get(str(name).strip().lower())
            if resolved_id is not None:
                ids.append(resolved_id)
            else:
                logger.warning(f"Carte non trouvée dans la base de données : '{name}'. Utilisation d'un Mock ID.")
                ids.append(DEFAULT_MOCK_ID)
                
        return ids
