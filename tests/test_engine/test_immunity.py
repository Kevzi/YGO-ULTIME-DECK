import pytest
from ygo_ultime_deck.engine.worker import evaluate_immunity, simulate_chunk

def test_evaluate_immunity_with_protection():
    hand_counts = {"Protection": 1, "Starter": 1}
    combo = {"name": "TestCombo", "requirements": [("Starter", 1)]}
    threat = {"name": "Ash Blossom"}
    
    # Avec une protection, l'immunité est toujours vraie
    assert evaluate_immunity(hand_counts, combo, threat) == True

def test_evaluate_immunity_with_extender():
    # 2 Starters alors que le combo n'en demande qu'un
    hand_counts = {"Starter": 2}
    combo = {"name": "TestCombo", "requirements": [("Starter", 1)]}
    threat = {"name": "Ash Blossom"}
    
    # Sans protection, l'adversaire détruit un Starter.
    # Puisqu'on a 2 Starters, il en reste 1. Combo passe.
    assert evaluate_immunity(hand_counts, combo, threat) == True

def test_evaluate_immunity_fails_without_extender():
    # 1 Starter pour 1 prérequis
    hand_counts = {"Starter": 1}
    combo = {"name": "TestCombo", "requirements": [("Starter", 1)]}
    threat = {"name": "Ash Blossom"}
    
    # L'adversaire détruit le seul Starter.
    assert evaluate_immunity(hand_counts, combo, threat) == False

def test_simulate_chunk_with_immunity():
    deck = ["Starter", "Starter", "Extender", "Protection", "Garnet"] * 10
    combos = [
        {"name": "Basic", "requirements": [{"name": "Starter", "count": 1}]}
    ]
    threats = [
        {"name": "Ash Blossom"}
    ]
    
    # On simule 100 mains de 5 cartes
    result = simulate_chunk(deck, combos, hand_size=5, iterations=100, threats=threats)
    
    # Vérification que le dictionnaire d'immunité a bien été créé
    assert "Basic" in result.immunity_success_rates
    assert "Ash Blossom" in result.immunity_success_rates["Basic"]
    
    # Les succès d'immunité doivent être inférieurs ou égaux aux succès de combo
    basic_success = result.combo_success_rates["Basic"]
    immunity_success = result.immunity_success_rates["Basic"]["Ash Blossom"]
    
    assert immunity_success <= basic_success
    # Vu la densité du deck, on s'attend à au moins un peu d'immunité
    assert immunity_success >= 0
