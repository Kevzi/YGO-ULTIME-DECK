import asyncio
import concurrent.futures
import os
import math
from typing import List
from rich.progress import Progress

from ygo_ultime_deck.models.simulation import SimulationRequest, SimulationResult
from ygo_ultime_deck.engine.worker import simulate_chunk

async def run_monte_carlo_simulation(deck: List[str], request: SimulationRequest, hand_size: int = 5, iterations: int = 100000, workers: int = None, threats: List[dict] = None) -> SimulationResult:
    """
    Run the Monte-Carlo simulation using ProcessPoolExecutor.
    """
    if hand_size < 0:
        raise ValueError("hand_size must be >= 0")
    if workers is not None and workers <= 0:
        raise ValueError("workers must be > 0")

    if workers is None:
        workers = os.cpu_count() or 4

    # Calculate iterations per worker
    chunk_size = math.ceil(iterations / workers)
    chunks = []
    remaining = iterations
    
    for i in range(workers):
        current_chunk = min(chunk_size, remaining)
        if current_chunk > 0:
            chunks.append(current_chunk)
            remaining -= current_chunk

    # Serialize combos to dicts to be picklable and pure
    combos_data = [combo.model_dump() for combo in request.combos]

    loop = asyncio.get_running_loop()
    
    total_result = SimulationResult(
        total_iterations=0, 
        combo_success_rates={c.name: 0 for c in request.combos},
        immunity_success_rates={c.name: {} for c in request.combos}
    )
    if threats:
        for c in request.combos:
            for t in threats:
                t_name = t.get("name", "Unknown")
                total_result.immunity_success_rates[c.name][t_name] = 0

    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        # We use a progress bar
        with Progress() as progress:
            task = progress.add_task("[green]Simulation Monte-Carlo...", total=iterations)
            
            futures = []
            for chunk_iterations in chunks:
                # Submit tasks
                future = loop.run_in_executor(
                    executor, 
                    simulate_chunk, 
                    deck, 
                    combos_data, 
                    hand_size, 
                    chunk_iterations,
                    threats
                )
                futures.append(future)
            
            # Wait for all tasks to complete and update progress dynamically
            for completed_future in asyncio.as_completed(futures):
                chunk_result = await completed_future
                # Aggregate results
                total_result.total_iterations += chunk_result.total_iterations
                for combo_name, successes in chunk_result.combo_success_rates.items():
                    total_result.combo_success_rates[combo_name] += successes
                for combo_name, threat_dict in chunk_result.immunity_success_rates.items():
                    target_threat_dict = total_result.immunity_success_rates.setdefault(combo_name, {})
                    for threat_name, successes in threat_dict.items():
                        target_threat_dict[threat_name] = target_threat_dict.get(threat_name, 0) + successes
                
                progress.advance(task, chunk_result.total_iterations)

    return total_result
