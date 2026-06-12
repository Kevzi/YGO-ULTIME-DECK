from ygo_ultime_deck.engine.resolver import CardResolver
from pathlib import Path

cache_path = Path("data/cache/aggregate.zip")
resolver = CardResolver(cache_path)

print(resolver.resolve_ids_to_names(["17209452"]))
