import pytest
from ygo_ultime_deck.engine.optimizer import optimize_deck_size

def test_optimize_zero_garnets():
    # Avec 0 garnets, on veut toujours maximiser les starters, donc la taille minimale (40)
    result = optimize_deck_size(starters_count=10, garnets_count=0, core_size=30)
    assert result["optimal_size"] == 40
    assert result["metrics"]["p_no_garnet"] == 1.0

def test_optimize_many_garnets_many_starters():
    # 20 starters, 10 garnets. P(Starter >= 1) sera très élevé même à 60 cartes.
    # L'optimum devrait tendre vers 60 pour diluer les 10 garnets.
    result = optimize_deck_size(starters_count=20, garnets_count=10, core_size=30)
    assert result["optimal_size"] > 40
    # Vérifions que le score à la taille optimale est le meilleur parmi les valides
    valid_results = [r for r in result["all_results"] if r["p_starter"] >= 0.85]
    best_no_garnet = max(r["p_no_garnet"] for r in valid_results)
    assert result["metrics"]["p_no_garnet"] == best_no_garnet

def test_optimize_forces_smaller_deck_for_consistency():
    # Très peu de starters (ex: 6). À 40 cartes, P(Starter) ~ 0.57 < 0.85.
    # Puisque aucun deck n'atteint 85%, il doit choisir le deck avec le meilleur score combiné,
    # ce qui favorise les petits decks car P(Starter) chute vite.
    result = optimize_deck_size(starters_count=6, garnets_count=2, core_size=20)
    # Dans ce cas, la perte de consistance du starter est punie par la multiplication du score.
    # L'optimum devrait être proche de 40.
    assert result["optimal_size"] == 40

def test_optimize_core_size_exceeds_min():
    # Core size de 45 cartes. Le deck minimum possible est 45.
    result = optimize_deck_size(starters_count=12, garnets_count=3, core_size=45)
    assert result["all_results"][0]["size"] == 45
    assert result["optimal_size"] >= 45

def test_optimize_core_size_exceeds_max():
    with pytest.raises(ValueError, match="minimum effectif"):
        optimize_deck_size(starters_count=12, garnets_count=3, core_size=65)

def test_optimize_min_exceeds_max():
    with pytest.raises(ValueError, match="ne peut pas être supérieur"):
        optimize_deck_size(starters_count=10, garnets_count=0, core_size=40, min_deck=60, max_deck=40)

def test_optimize_negative_values():
    with pytest.raises(ValueError, match="négatives ne sont pas autorisées"):
        optimize_deck_size(starters_count=-1, garnets_count=0, core_size=40)

def test_optimize_zero_starters():
    with pytest.raises(ValueError, match="Impossible d'optimiser"):
        optimize_deck_size(starters_count=0, garnets_count=5, core_size=40)

def test_optimize_crosses_85_threshold():
    # 9 starters for 40 cards gives 74% (fails)
    # Let's find a case where increasing deck size drops below 85%
    # e.g., 14 starters at 40 cards = 0.89. 
    # At 50 cards, 14 starters = 0.82 (fails).
    # It should pick a size somewhere between 40 and 49 that maximizes score.
    result = optimize_deck_size(starters_count=14, garnets_count=5, core_size=40)
    # The optimal size MUST be the one that gives at least 85%.
    assert result["metrics"]["p_starter"] >= 0.85
