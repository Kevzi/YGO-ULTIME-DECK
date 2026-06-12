import random
import re
from typing import List, Dict, Any
from ygo_ultime_deck.models.simulation import SimulationResult

DRAW_REGEX = re.compile(r"^(?:Draw|Excavate)-(\d+)$", re.IGNORECASE)

def evaluate_immunity(hand_counts: Dict[str, int], combo: Dict[str, Any], threat: Dict[str, Any]) -> bool:
    """
    Évalue si la main survit à une menace.
    - Si la main possède une 'Protection', la menace est annulée (Succès).
    - Sinon, l'adversaire détruit une pièce du combo.
    """
    if hand_counts.get("Protection", 0) > 0:
        return True
        
    category = threat.get("category", "Generic")
    reqs_to_check = combo.get("requirements", [])
    
    # Un Handtrap cible typiquement les Starters.
    if category == "Handtrap":
        starters = [req for req in reqs_to_check if req[0].lower() == "starter"]
        if starters:
            reqs_to_check = starters
            
    for req_name, req_count in reqs_to_check:
        if hand_counts.get(req_name, 0) <= req_count:
            return False
            
    return True

def simulate_chunk(deck: List[str], combos: List[Dict[str, Any]], hand_size: int, iterations: int, threats: List[Dict[str, Any]] = None) -> SimulationResult:
    """
    Pure function to simulate a chunk of hands.
    deck: List of card names/tags.
    combos: List of combo definitions (dicts for easy serialization).
    hand_size: Number of cards to draw.
    iterations: Number of hands to simulate.
    """
    combo_successes = {combo["name"]: 0 for combo in combos}
    immunity_successes = {combo["name"]: {} for combo in combos}
    if threats:
        for combo in combos:
            for threat in threats:
                t_name = threat.get("name", "Unknown")
                immunity_successes[combo["name"]][t_name] = 0

    # Pre-parse requirements to avoid inner loop overhead
    parsed_combos = []
    for combo in combos:
        parsed_reqs = []
        for req in combo.get("requirements", []):
            if isinstance(req, dict):
                try:
                    count = int(req.get("count", 1))
                except (ValueError, TypeError):
                    count = 1
                if req.get("name"):
                    parsed_reqs.append((req.get("name"), count))
            elif isinstance(req, (list, tuple)) and len(req) == 2:
                parsed_reqs.append((req[0], int(req[1])))
        parsed_combos.append({"name": combo["name"], "requirements": parsed_reqs})

    deck_size = len(deck)

    for _ in range(iterations):
        # We need to sample hand_size + any extra cards. But we don't know the extra cards until we check the hand.
        # Sampling the whole deck size is fast enough for small lists, but to be truly optimal and avoid deck[:] slice,
        # we can just use random.sample for the initial hand, and if we need more, sample from the remainder.
        # But `random.sample` returns a list, computing the remainder is O(N).
        # A simple optimization: for YGO decks (40-60 cards), `random.sample(deck, deck_size)` creates a shuffled copy.
        # It is actually faster to just `random.sample(deck, deck_size)` than `deck[:]` and `random.shuffle`.
        shuffled_deck = random.sample(deck, deck_size)
        hand = shuffled_deck[:hand_size]
        
        hand_counts = {}
        total_draw = 0
        for card in hand:
            hand_counts[card] = hand_counts.get(card, 0) + 1
            match = DRAW_REGEX.match(card)
            if match:
                total_draw += int(match.group(1))

        failed_combos = []
        for combo in parsed_combos:
            success = True
            for req_name, req_count in combo["requirements"]:
                if hand_counts.get(req_name, 0) < req_count:
                    success = False
                    break
            
            if success:
                combo_successes[combo["name"]] += 1
                if threats:
                    for threat in threats:
                        if evaluate_immunity(hand_counts, combo, threat):
                            immunity_successes[combo["name"]][threat.get("name", "Unknown")] += 1
            else:
                failed_combos.append(combo)
                
        if failed_combos and total_draw > 0:
            draw_negated = False
            if threats:
                for threat in threats:
                    if threat.get("category") == "Handtrap" and hand_counts.get("Protection", 0) == 0:
                        draw_negated = True
                        break
                        
            if not draw_negated:
                extra_cards = shuffled_deck[hand_size:hand_size + total_draw]
                for card in extra_cards:
                    hand_counts[card] = hand_counts.get(card, 0) + 1
                
            for combo in failed_combos:
                success = True
                for req_name, req_count in combo["requirements"]:
                    if hand_counts.get(req_name, 0) < req_count:
                        success = False
                        break
                if success:
                    combo_successes[combo["name"]] += 1
                    if threats:
                        for threat in threats:
                            if evaluate_immunity(hand_counts, combo, threat):
                                immunity_successes[combo["name"]][threat.get("name", "Unknown")] += 1

    return SimulationResult(
        total_iterations=iterations,
        combo_success_rates=combo_successes,
        immunity_success_rates=immunity_successes
    )
