from typing import Tuple, Dict, Any, List
from ygo_ultime_deck.engine.math_utils import calculate_hypergeometric

def get_probability_at_least_one(deck_size: int, success_count: int, hand_size: int) -> float:
    """
    Calcule la probabilité de piocher AU MOINS 1 exemplaire de la carte voulue.
    P(X >= 1) = 1 - P(X == 0)
    """
    if success_count == 0:
        return 0.0
    prob_zero = calculate_hypergeometric(deck_size, success_count, hand_size, 0)
    return 1.0 - prob_zero

def get_probability_exactly_zero(deck_size: int, success_count: int, hand_size: int) -> float:
    """
    Calcule la probabilité de n'en piocher AUCUN.
    """
    if success_count == 0:
        return 1.0
    return calculate_hypergeometric(deck_size, success_count, hand_size, 0)

def optimize_deck_size(
    starters_count: int, 
    garnets_count: int, 
    core_size: int, 
    hand_size: int = 5,
    min_deck: int = 40,
    max_deck: int = 60,
    starter_threshold: float = 0.85
) -> Dict[str, Any]:
    """
    Détermine la taille de deck optimale (entre min_deck et max_deck).
    Objectif :
    1. Maintenir P(Starter >= 1) >= starter_threshold
    2. Maximiser P(Garnet == 0)
    
    Si aucun deck ne satisfait le threshold, on favorise la consistance du starter.
    Si garnets_count == 0, on favorise toujours la taille minimale (40) pour maximiser les starters.
    """
    best_size = min_deck
    best_score = -1.0
    
    results = []
    
    # Validation des entrées
    if min_deck > max_deck:
        raise ValueError(f"min_deck ({min_deck}) ne peut pas être supérieur à max_deck ({max_deck}).")
    if starters_count < 0 or garnets_count < 0 or core_size < 0 or hand_size < 0:
        raise ValueError("Les valeurs négatives ne sont pas autorisées pour les cartes.")
    if starters_count == 0:
        raise ValueError("Impossible d'optimiser un deck avec 0 starters.")
        
    actual_min = max(min_deck, core_size)
    if actual_min > max_deck:
        raise ValueError(f"Le minimum effectif ({actual_min}) dépasse la taille maximale autorisée ({max_deck}). Vérifiez min_deck ou core_size.")

    for size in range(actual_min, max_deck + 1):
        if starters_count + garnets_count > size:
            continue # Configuration impossible
            
        p_starter = get_probability_at_least_one(size, starters_count, hand_size)
        p_no_garnet = get_probability_exactly_zero(size, garnets_count, hand_size)
        
        # Si aucun garnet, le score est juste la proba des starters (donc 40 sera toujours gagnant)
        if garnets_count == 0:
            score = p_starter
        else:
            # Score heuristique combiné : probabilité de (Starter ET Pas de Garnet)
            # (Simplifié en multiplication. Note: ce n'est pas une probabilité mathématique
            # exacte car les événements sont dépendants, mais c'est une heuristique de scoring).
            score = p_starter * p_no_garnet
            
        results.append({
            "size": size,
            "p_starter": p_starter,
            "p_no_garnet": p_no_garnet,
            "score": score
        })

    # Filtrer ceux qui respectent le threshold
    valid_sizes = [res for res in results if res["p_starter"] >= starter_threshold]
    
    if valid_sizes:
        # L'objectif est de maximiser le score combiné sous la contrainte des starters
        best_result = max(valid_sizes, key=lambda x: x["score"])
    else:
        # Aucun ne respecte le threshold, on doit privilégier la consistance brute (p_starter).
        # On ne se fie pas au score combiné car diluer les briques détruirait encore plus le deck.
        if not results:
            raise ValueError("Aucune taille de deck valide ne peut contenir ces cartes.")
        best_result = max(results, key=lambda x: x["p_starter"])

    return {
        "optimal_size": best_result["size"],
        "metrics": best_result,
        "all_results": results
    }
