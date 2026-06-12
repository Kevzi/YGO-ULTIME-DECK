"""Module Scout pour interroger Yugipedia et extraire des contres potentiels."""

import httpx
import re
import asyncio
from typing import List, Dict, Optional

YUGIPEDIA_API_URL = "https://yugipedia.com/api.php"

# Mots-clés indiquant une interaction de contre ou de faiblesse
COUNTER_KEYWORDS = [
    r"counter", r"negate", r"banish", r"destroy", r"prevent",
    r"weakness", r"vulnerable", r"stop", r"tribute", r"out"
]

async def fetch_card_tips(card_name: str) -> Optional[str]:
    """
    Interroge l'API Yugipedia pour obtenir le contenu brut de la page Card_Tips de la carte.
    """
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
                    # Page non trouvée
                    return None
                    
                revisions = page_info.get("revisions", [])
                if revisions:
                    return revisions[0].get("*", "")
                    
            return None
        except Exception as e:
            print(f"Erreur lors de la requête Yugipedia pour {card_name}: {e}")
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

def analyze_tips_for_counters(tips_text: str) -> List[str]:
    """
    Analyse le texte brut de la page Card_Tips pour isoler les "Ultimate Staples" potentielles.
    Utilise des Regex sur les phrases pour identifier le contexte (Contre/Faiblesse).
    """
    if not tips_text:
        return []
        
    found_counters = set()
    
    # Découper le texte en phrases ou lignes (les listes sont souvent sur une ligne)
    lines = tips_text.split('\n')
    
    # Construire la regex combinée pour les mots-clés
    pattern = re.compile(r'\b(?:' + '|'.join(COUNTER_KEYWORDS) + r')\b', re.IGNORECASE)
    
    for line in lines:
        if pattern.search(line):
            # Si la ligne contient un mot-clé de contre, on extrait toutes les cartes mentionnées
            cards = extract_cards_from_wikitext(line)
            found_counters.update(cards)
            
    return list(found_counters)

async def scout_card(card_name: str) -> Dict[str, any]:
    """
    Orchestre la récupération et l'analyse pour une carte donnée.
    """
    tips_text = await fetch_card_tips(card_name)
    if not tips_text:
        return {"card": card_name, "found": False, "counters": []}
        
    counters = analyze_tips_for_counters(tips_text)
    return {"card": card_name, "found": True, "counters": counters}
