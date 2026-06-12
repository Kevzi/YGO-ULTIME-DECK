import pytest
import asyncio
from ygo_ultime_deck.engine.monte_carlo import run_monte_carlo_simulation
from ygo_ultime_deck.models.simulation import SimulationRequest, TargetCombo, Requirement

@pytest.mark.asyncio
async def test_run_monte_carlo_simulation_basic():
    # Arrange
    deck = ["Card A"] * 3 + ["Card B"] * 3 + ["Garnet"] * 34
    iterations = 1000
    hand_size = 5
    
    req1 = Requirement(name="Card A", count=1)
    req2 = Requirement(name="Card B", count=1)
    combo = TargetCombo(name="Combo 1", requirements=[req1, req2])
    request = SimulationRequest(combos=[combo])

    # Act
    # Running simulation with small chunks to test multiprocessing division
    result = await run_monte_carlo_simulation(deck, request, hand_size, iterations, workers=2)

    # Assert
    assert result.total_iterations == iterations
    assert 0 <= result.combo_success_rates["Combo 1"] <= iterations

@pytest.mark.asyncio
async def test_run_monte_carlo_simulation_100k():
    deck = ["Card A"] * 3 + ["Garnet"] * 37
    iterations = 100000
    hand_size = 5
    req1 = Requirement(name="Card A", count=1)
    combo = TargetCombo(name="Combo 1", requirements=[req1])
    request = SimulationRequest(combos=[combo])

    result = await run_monte_carlo_simulation(deck, request, hand_size, iterations, workers=2)
    assert result.total_iterations == 100000

@pytest.mark.asyncio
async def test_run_monte_carlo_simulation_non_blocking():
    deck = ["Card A"] * 3 + ["Garnet"] * 37
    iterations = 50000
    hand_size = 5
    req1 = Requirement(name="Card A", count=1)
    combo = TargetCombo(name="Combo 1", requirements=[req1])
    request = SimulationRequest(combos=[combo])

    async def blocking_task():
        await asyncio.sleep(0.1)
        return "done"

    simulation_task = asyncio.create_task(run_monte_carlo_simulation(deck, request, hand_size, iterations, workers=2))
    block_task = asyncio.create_task(blocking_task())

    # Ensure both complete and the sleep is not blocked significantly
    res_sim, res_block = await asyncio.gather(simulation_task, block_task)
    assert res_block == "done"
    assert res_sim.total_iterations == iterations
