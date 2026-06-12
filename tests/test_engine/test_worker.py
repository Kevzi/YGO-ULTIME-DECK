import pytest
from unittest.mock import patch
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

def test_simulate_chunk_draw_generator():
    deck = ["Card A", "Draw-2", "Garnet1", "Garnet2", "Garnet3", "Card B", "Card C"]
    iterations = 1
    hand_size = 5
    combos = [
        {"name": "Combo 1", "requirements": [{"name": "Card A", "count": 1}, {"name": "Card B", "count": 1}]}
    ]

    with patch('ygo_ultime_deck.engine.worker.random.sample') as mock_sample:
        # random.sample should return the shuffled deck (all 7 cards)
        # The first 5 are the hand, the next 2 are drawn by Draw-2
        mock_sample.return_value = ["Card A", "Draw-2", "Garnet1", "Garnet2", "Garnet3", "Card B", "Card C"]
        result = simulate_chunk(deck, combos, hand_size, iterations)

    assert result.total_iterations == iterations
    assert result.combo_success_rates["Combo 1"] == 1

def test_out_of_bounds_draw():
    # A deck of 6 cards. Hand size 5. Only 1 card remains.
    # But hand has Draw-2. It should draw the 1 remaining card without crashing.
    deck = ["Card A", "Draw-2", "Garnet1", "Garnet2", "Garnet3", "Card B"]
    iterations = 1
    hand_size = 5
    combos = [
        {"name": "Combo 1", "requirements": [{"name": "Card A", "count": 1}, {"name": "Card B", "count": 1}]}
    ]

    with patch('ygo_ultime_deck.engine.worker.random.sample') as mock_sample:
        mock_sample.return_value = ["Card A", "Draw-2", "Garnet1", "Garnet2", "Garnet3", "Card B"]
        result = simulate_chunk(deck, combos, hand_size, iterations)

    # It shouldn't crash, and Card B should be found.
    assert result.total_iterations == iterations
    assert result.combo_success_rates["Combo 1"] == 1

