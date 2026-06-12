import random
from typing import List, Dict, Any
from ygo_ultime_deck.models.simulation import SimulationResult

def simulate_chunk(deck: List[str], combos: List[Dict[str, Any]], hand_size: int, iterations: int) -> SimulationResult:
    """
    Pure function to simulate a chunk of hands.
    deck: List of card names/tags.
    combos: List of combo definitions (dicts for easy serialization).
    hand_size: Number of cards to draw.
    iterations: Number of hands to simulate.
    """
    combo_successes = {combo["name"]: 0 for combo in combos}

    # Pre-parse requirements to avoid inner loop overhead
    parsed_combos = []
    for combo in combos:
        parsed_reqs = []
        for req in combo.get("requirements", []):
            try:
                count = int(req.get("count", 1))
            except (ValueError, TypeError):
                count = 1
            if req.get("name"):
                parsed_reqs.append((req.get("name"), count))
        parsed_combos.append({"name": combo["name"], "requirements": parsed_reqs})

    for _ in range(iterations):
        hand = random.sample(deck, k=hand_size)
        hand_counts = {}
        for card in hand:
            hand_counts[card] = hand_counts.get(card, 0) + 1

        for combo in parsed_combos:
            success = True
            for req_name, req_count in combo["requirements"]:
                if hand_counts.get(req_name, 0) < req_count:
                    success = False
                    break
            
            if success:
                combo_successes[combo["name"]] += 1

    return SimulationResult(
        total_iterations=iterations,
        combo_success_rates=combo_successes
    )
