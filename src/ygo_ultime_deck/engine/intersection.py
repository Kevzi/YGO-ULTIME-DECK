import asyncio
from pathlib import Path
from typing import List, Dict, Set
from collections import Counter
import logging

from ygo_ultime_deck.engine.resolver import CardResolver
from ygo_ultime_deck.ingestion.parser import load_and_parse_ygojson
from ygo_ultime_deck.rules.tagger import RegexTagger
from ygo_ultime_deck.ingestion.scout import scout_card

logger = logging.getLogger(__name__)

# Liste des tags valides pour scouter (on ignore Garnet, Generic, etc.)
VALID_SCOUT_TAGS = {"Starter", "Extender"}

def parse_ydk_ids(deck_file: Path) -> Dict[str, List[str]]:
    """Parse un fichier YDK et sépare les IDs du Main et Extra deck."""
    result = {"main": [], "extra": []}
    if not deck_file.exists():
        return result
        
    current_section = None
    with open(deck_file, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#main"):
                current_section = "main"
            elif line.startswith("#extra"):
                current_section = "extra"
            elif line.startswith("!side"):
                current_section = "side"
            elif line.isdigit() and current_section in ["main", "extra"]:
                result[current_section].append(line)
                
    return result

async def analyze_meta(deck_files: List[Path], cache_path: Path) -> Dict[str, any]:
    """
    Analyse plusieurs decks méta pour extraire les pires contres communs.
    Utilise le RegexTagger pour filtrer les cibles pertinentes.
    """
    # 1. Charger la base de données de cartes complète pour le Tagger
    logger.info("Chargement de YGOJSON pour le RegexTagger...")
    all_cards = load_and_parse_ygojson(cache_path)
    card_dict = {str(c.id): c for c in all_cards}
    # Aussi par mot de passe pour les IDs YDK
    for c in all_cards:
        pwds = getattr(c, "passwords", []) or [] # fallback if not present, but load_and_parse_ygojson doesn't parse passwords actually!
        # Wait, CardModel might not have passwords. We can use CardResolver to map YDK IDs to names, then map names to CardModel.
        
    resolver = CardResolver(cache_path)
    tagger = RegexTagger.from_config()
    
    # 2. Collecter les IDs uniques à scouter
    cards_to_scout_names = set()
    
    for deck_file in deck_files:
        ydk_data = parse_ydk_ids(deck_file)
        
        # Pour l'Extra Deck, on scoute tout !
        if ydk_data["extra"]:
            extra_names = resolver.resolve_ids_to_names(ydk_data["extra"])
            for name in extra_names:
                if name != "Inconnu":
                    cards_to_scout_names.add(name)
                    
        # Pour le Main Deck, on utilise le RegexTagger
        main_names = resolver.resolve_ids_to_names(ydk_data["main"])
        for name in main_names:
            if name == "Inconnu":
                continue
            
            # Trouver le CardModel par nom
            card_model = next((c for c in all_cards if str(c.name).lower() == name.lower()), None)
            if card_model:
                # Appliquer le tagger
                tagged_card = tagger.tag_card(card_model)
                tags = set(tagged_card.tags)
                
                # Si c'est un Starter ou Extender, on scoute.
                if tags.intersection(VALID_SCOUT_TAGS):
                    cards_to_scout_names.add(name)
    
    logger.info(f"{len(cards_to_scout_names)} cartes stratégiques identifiées pour le scouting.")
    
    # 3. Lancer le Scout asynchrone sur toutes ces cartes
    scout_tasks = [scout_card(name) for name in cards_to_scout_names]
    scout_results = await asyncio.gather(*scout_tasks)
    
    # 4. Agréger et pondérer les contres (Intersection)
    counter_freq = Counter()
    
    for res in scout_results:
        if res["found"]:
            for counter in res["counters"]:
                # Pondération : +1 de base
                weight = 1
                
                # Chercher le CardModel pour voir si c'est une Hand_Trap / Board_Breaker
                counter_model = next((c for c in all_cards if str(c.name).lower() == counter.lower()), None)
                if counter_model:
                    t_card = tagger.tag_card(counter_model)
                    t_tags = set(t_card.tags)
                    if "Hand_Trap" in t_tags or "Board_Breaker" in t_tags or "Generic" in t_tags:
                        weight = 3  # Multiplicateur pour les staples génériques
                        
                counter_freq[counter] += weight
                
    # Extraire le Top 10 des "Ultimate Staples"
    top_staples = [c[0] for c in counter_freq.most_common(10)]
    
    return {
        "scouted_cards_count": len(cards_to_scout_names),
        "top_counters": counter_freq.most_common(15),
        "ultimate_staples": top_staples
    }

async def find_matching_archetypes(staples: List[str]) -> List[tuple]:
    """
    Reverse-Scouting : Prend les meilleures staples de contre, et cherche leurs synergies.
    """
    synergy_freq = Counter()
    
    scout_tasks = [scout_card(staple) for staple in staples]
    scout_results = await asyncio.gather(*scout_tasks)
    
    for res in scout_results:
        if res["found"]:
            for synergy in res["synergies"]:
                # Éviter de se recommander soi-même
                if synergy.lower() not in [s.lower() for s in staples]:
                    synergy_freq[synergy] += 1
                    
    return synergy_freq.most_common(10)
