"""Module Scout pour interroger Yugipedia et extraire des contres potentiels."""

import httpx
import re
import asyncio
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

YUGIPEDIA_API_URL = "https://yugipedia.com/api.php"

# Mots-clés indiquant une interaction de contre ou de faiblesse
COUNTER_KEYWORDS = [
    r"counter", r"negate", r"banish", r"destroy", r"prevent",
    r"weakness", r"vulnerable", r"stop", r"tribute", r"out"
]

# Mots-clés indiquant une synergie ou un combo
SYNERGY_KEYWORDS = [
    r"synergy", r"combo", r"search", r"add", r"summon",
    r"works well", r"recommend", r"combo with", r"special summon"
]

async def fetch_card_tips(card_name: str) -> Optional[str]:
    """
    Interroge l'API Yugipedia pour obtenir le contenu brut de la page Card_Tips de la carte,
    avec un système de cache local pour éviter le ban de l'IP.
    """
    # Chemin du cache
    cache_dir = Path(__file__).resolve().parent.parent.parent.parent / "data" / "cache" / "yugipedia"
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # Nom de fichier sain
    safe_name = re.sub(r'[\\/*?:"<>|]', "", card_name)
    cache_file = cache_dir / f"{safe_name}.json"
    
    if cache_file.exists():
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("tips_text")
        except json.JSONDecodeError:
            pass # Fichier corrompu, on re-télécharge
            
    # Remplacer les espaces par des underscores pour le titre MediaWiki
    title = f"Card_Tips:{card_name.replace(' ', '_')}"
    
    params = {
        "action": "query",
        "prop": "revisions",
        "rvprop": "content",
        "titles": title,
        "format": "json"
    }
    
    headers = {
        "User-Agent": "YGO-Ultime-Deck-Scout/1.0 (https://github.com/Kevzi/YGO-ULTIME-DECK)"
    }
    
    async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
        try:
            response = await client.get(YUGIPEDIA_API_URL, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            pages = data.get("query", {}).get("pages", {})
            for page_id, page_info in pages.items():
                if int(page_id) < 0:
                    # Mettre en cache l'absence de page pour ne pas re-requêter
                    with open(cache_file, "w", encoding="utf-8") as f:
                        json.dump({"tips_text": None}, f)
                    return None
                    
                revisions = page_info.get("revisions", [])
                if revisions:
                    tips_text = revisions[0].get("*", "")
                    with open(cache_file, "w", encoding="utf-8") as f:
                        json.dump({"tips_text": tips_text}, f)
                    return tips_text
                    
            return None
        except Exception as e:
            logger.error(f"Erreur lors de la requête Yugipedia pour {card_name}: {e}")
            return None

def extract_cards_from_wikitext(text: str) -> List[str]:
    """
    Extrait les noms de cartes des liens MediaWiki ou templates Yugipedia.
    Exemples: [[Ash Blossom & Joyous Spring]] ou {{Card|Effect Veiler}}
    """
    cards = set()
    
    # Liens wikis standards: [[Card Name]] ou [[Card Name|Display text]]
    wiki_links = re.findall(r"\[\[([^\]\|]+)(?:\|[^\]]+)?\]\]", text)
    for link in wiki_links:
        # Filtrer les liens non-cartes (Category, File, etc.)
        if ":" not in link:
            cards.add(link.strip())
            
    # Templates Yugipedia: {{Card|Card Name}} ou {{cgnd|Card Name}}
    templates = re.findall(r"\{\{(?:Card|cgnd)\|([^}]+)\}\}", text, flags=re.IGNORECASE)
    for tpl in templates:
        cards.add(tpl.strip())
        
    return list(cards)

def analyze_tips_for_counters(tips_text: str) -> Dict[str, List[str]]:
    """
    Analyse le texte brut de la page Card_Tips pour isoler les contres et les synergies.
    """
    if not tips_text:
        return {"counters": [], "synergies": []}
        
    found_counters = set()
    found_synergies = set()
    
    # Découper le texte en phrases ou lignes (les listes sont souvent sur une ligne)
    lines = tips_text.split('\n')
    
    counter_pattern = re.compile(r'\b(?:' + '|'.join(COUNTER_KEYWORDS) + r')\b', re.IGNORECASE)
    synergy_pattern = re.compile(r'\b(?:' + '|'.join(SYNERGY_KEYWORDS) + r')\b', re.IGNORECASE)
    
    for line in lines:
        is_counter = counter_pattern.search(line)
        is_synergy = synergy_pattern.search(line)
        
        # Si la ligne contient un mot-clé, on extrait toutes les cartes mentionnées
        if is_counter or is_synergy:
            cards = extract_cards_from_wikitext(line)
            if is_counter and not is_synergy:
                found_counters.update(cards)
            elif is_synergy and not is_counter:
                found_synergies.update(cards)
            else:
                # Si les deux mots-clés sont présents (ambigu), on met par défaut dans synergies
                # car Card_Tips parle souvent de synergies.
                found_synergies.update(cards)
            
    return {
        "counters": list(found_counters),
        "synergies": list(found_synergies)
    }

async def scout_card(card_name: str) -> Dict[str, any]:
    """
    Orchestre la récupération et l'analyse pour une carte donnée.
    """
    tips_text = await fetch_card_tips(card_name)
    if not tips_text:
        return {"card": card_name, "found": False, "counters": [], "synergies": []}
        
    analysis = analyze_tips_for_counters(tips_text)
    return {
        "card": card_name, 
        "found": True, 
        "counters": analysis["counters"],
        "synergies": analysis["synergies"]
    }
