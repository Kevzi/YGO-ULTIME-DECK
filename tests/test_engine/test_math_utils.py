import pytest
import math
from ygo_ultime_deck.engine.math_utils import calculate_hypergeometric, log_binom

def test_log_binom():
    # 5 choose 2 = 10
    # log(10) ~ 2.302585
    val = math.exp(log_binom(5, 2))
    assert math.isclose(val, 10.0, rel_tol=1e-5)

def test_calculate_hypergeometric_simple():
    # Deck of 40 (N), 3 copies of card (K), draw 5 (n), want exactly 1 (k)
    # math: C(3, 1) * C(37, 4) / C(40, 5)
    # C(3, 1) = 3
    # C(37, 4) = 66045
    # C(40, 5) = 658008
    # prob = 3 * 66045 / 658008 = 0.3011118
    prob = calculate_hypergeometric(40, 3, 5, 1)
    assert math.isclose(prob, 0.3011118, rel_tol=1e-4)

def test_calculate_hypergeometric_zero_k():
    # Want exactly 0 copies
    prob = calculate_hypergeometric(40, 3, 5, 0)
    # C(3, 0) * C(37, 5) / C(40, 5)
    # 1 * 435897 / 658008 = 0.662449
    assert math.isclose(prob, 0.662449, rel_tol=1e-4)

def test_calculate_hypergeometric_impossible():
    # Draw 5, want 6 copies (impossible)
    prob = calculate_hypergeometric(40, 3, 5, 6)
    assert prob == 0.0

    # Draw more copies than in deck
    prob2 = calculate_hypergeometric(40, 3, 5, 4)
    assert prob2 == 0.0

    # Draw from 0 sample size
    prob3 = calculate_hypergeometric(40, 3, 0, 1)
    assert prob3 == 0.0

def test_calculate_hypergeometric_no_overflow_60_cards():
    # Deck of 60, draw 5, want 1 out of 3.
    prob = calculate_hypergeometric(60, 3, 5, 1)
    assert 0.0 <= prob <= 1.0
    
    # Extreme edge case: Deck of 1000, draw 100, want 1 out of 3.
    prob2 = calculate_hypergeometric(1000, 3, 100, 1)
    assert 0.0 <= prob2 <= 1.0

def test_calculate_hypergeometric_all():
    # Deck of 40, want exactly 5 out of 5
    prob = calculate_hypergeometric(40, 5, 5, 5)
    # 1 / 658008
    assert math.isclose(prob, 1 / 658008, rel_tol=1e-4)

def test_calculate_hypergeometric_stress_test():
    """
    Stress test verifying that massive sequential calls for combinatorial calculations
    over a 60-card deck do not trigger exceptions or memory errors.
    """
    deck_size = 60
    hand_size = 5
    successful_calls = 0
    
    # Simulate calculating multiple combinations repeatedly
    # e.g., iterating through a large dataset or monte carlo engine
    for k in range(0, 4):  # card copies in hand
        for total_targets in range(1, 15):  # varying target copies in deck
            for _ in range(100):  # Simulate many calls per branch
                prob = calculate_hypergeometric(deck_size, total_targets, hand_size, k)
                assert 0.0 <= prob <= 1.0
                successful_calls += 1
                
    # Ensure all loops completed successfully
    assert successful_calls == 4 * 14 * 100
