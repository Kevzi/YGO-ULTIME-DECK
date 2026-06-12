import json
import zipfile
from pathlib import Path

cache_path = Path("data/cache/aggregate.zip")

with zipfile.ZipFile(cache_path, 'r') as zf:
    json_filename = next((name for name in zf.namelist() if name.endswith('.json')), None)
    with zf.open(json_filename) as f:
        data = json.load(f)
        cards = data.get("data", []) if isinstance(data, dict) else data
        
        for c in cards:
            name = c.get("name", "")
            if "Kewl Tune" in name:
                print(f"Name: {name}, ID: {c.get('id')}")
