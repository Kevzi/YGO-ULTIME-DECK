import pytest
from ygo_ultime_deck.engine.worker import simulate_chunk

def test_simulate_chunk_basic():
    # Arrange
    deck = ["Card A"] * 3 + ["Card B"] * 3 + ["Garnet"] * 34
    iterations = 100
    hand_size = 5
    # The combo expects at least 1 "Card A" and 1 "Card B"
    combos = [
        {"name": "Combo 1", "requirements": [{"name": "Card A", "count": 1}, {"name": "Card B", "count": 1}]}
    ]

    # Act
    result = simulate_chunk(deck, combos, hand_size, iterations)

    # Assert
    assert result.total_iterations == iterations
    assert "Combo 1" in result.combo_success_rates
    assert 0 <= result.combo_success_rates["Combo 1"] <= iterations
