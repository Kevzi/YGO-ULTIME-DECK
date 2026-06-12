import pytest
import json
import zipfile
import logging
from pathlib import Path
from ygo_ultime_deck.engine.resolver import CardResolver, DEFAULT_MOCK_ID

def create_mock_zip(path: Path):
    data = {
        "data": [
            {"id": 14558127, "name": "Ash Blossom & Joyous Spring"},
            {"id": 86066372, "name": "Accesscode Talker"}
        ]
    }
    with zipfile.ZipFile(path, 'w') as zf:
        zf.writestr("cards.json", json.dumps(data))

def test_resolve_valid_names(tmp_path):
    zip_path = tmp_path / "aggregate.zip"
    create_mock_zip(zip_path)
    
    resolver = CardResolver(zip_path)
    ids = resolver.resolve(["Ash Blossom & Joyous Spring", "accesscode talker "])
    
    assert ids == [14558127, 86066372]

def test_resolve_invalid_name(tmp_path, caplog):
    zip_path = tmp_path / "aggregate.zip"
    create_mock_zip(zip_path)
    
    resolver = CardResolver(zip_path)
    
    with caplog.at_level(logging.WARNING):
        ids = resolver.resolve(["Carte Inexistante"])
        
    assert ids == [DEFAULT_MOCK_ID]
    assert "Carte non trouvée dans la base de données : 'Carte Inexistante'" in caplog.text

def test_resolve_missing_zip(tmp_path):
    resolver = CardResolver(tmp_path / "missing.zip")
    ids = resolver.resolve(["Ash Blossom"])
    assert ids == [DEFAULT_MOCK_ID]

def test_lazy_loading(tmp_path):
    zip_path = tmp_path / "aggregate.zip"
    create_mock_zip(zip_path)
    
    resolver = CardResolver(zip_path)
    assert resolver._loaded is False
    
    resolver.resolve(["Ash Blossom & Joyous Spring"])
    assert resolver._loaded is True
    
    # Second call should not reload
    zip_path.unlink() # Delete the file to prove it doesn't try to open it again
    ids = resolver.resolve(["Accesscode Talker"])
    assert ids == [86066372]
