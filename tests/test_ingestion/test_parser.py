"""Tests for the YGOJSON parser module."""

import pytest
import zipfile
import json

from ygo_ultime_deck.ingestion.parser import load_and_parse_ygojson
from ygo_ultime_deck.models.card import CardModel

@pytest.fixture
def mock_ygojson_zip(tmp_path):
    """Create a mock YGOJSON zip file in memory for testing."""
    mock_data = [
        # Valid TCG Card
        {
            "id": "12345678",
            "name": "Dark Magician",
            "type": "Normal Monster",
            "desc": "The ultimate wizard in terms of attack and defense.",
            "atk": 2500,
            "def": 2100,
            "level": 7,
            "race": "Spellcaster",
            "attribute": "DARK",
            "formats": ["TCG", "OCG"]
        },
        # Valid TCG Card with "?" stats
        {
            "id": "10000020",
            "name": "Slifer the Sky Dragon",
            "type": "Effect Monster",
            "desc": "Requires 3 Tributes to Normal Summon...",
            "atk": "?",
            "def": "?",
            "level": 10,
            "race": "Divine-Beast",
            "attribute": "DIVINE",
            "formats": ["TCG", "OCG"]
        },
        # Rush Duel Card (should be filtered out)
        {
            "id": "99999999",
            "name": "Rush Dragon",
            "type": "Effect Monster",
            "desc": "Rush Duel exclusive.",
            "formats": ["Rush Duel"]
        },
        # Token (should be filtered out)
        {
            "id": "88888888",
            "name": "Sheep Token",
            "type": "Token",
            "desc": "Special Summoned by Scapegoat.",
            "formats": ["TCG", "OCG"]
        },
        # Speed Duel only (should be filtered out)
        {
            "id": "77777777",
            "name": "Speed Spell",
            "type": "Spell Card",
            "desc": "Speed duel card.",
            "formats": ["Speed Duel"]
        },
        # Malformed Card (missing required fields, should not crash parser)
        {
            "name": "Missing ID Card",
            "type": "Effect Monster",
            "formats": ["TCG"]
        },
        # Banned Card (should be filtered out)
        {
            "id": "11111111",
            "name": "Pot of Greed",
            "type": "Spell Card",
            "desc": "Draw 2 cards.",
            "formats": ["TCG", "OCG"],
            "banlist_info": {
                "ban_tcg": "Banned",
                "ban_ocg": "Banned"
            }
        },
        # Malformed non-dictionary item
        "Just a string instead of a dictionary",
        12345
    ]

    zip_path = tmp_path / "aggregate.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("cards.json", json.dumps(mock_data))
        
    return zip_path

def test_load_and_parse_ygojson(mock_ygojson_zip):
    """Test that the parser correctly filters formats and handles errors."""
    cards = load_and_parse_ygojson(mock_ygojson_zip)
    
    assert len(cards) == 2
    assert all(isinstance(c, CardModel) for c in cards)
    
    names = [c.name for c in cards]
    assert "Dark Magician" in names
    assert "Slifer the Sky Dragon" in names
    
    # Check that "?" was properly converted to -1
    slifer = next(c for c in cards if c.name == "Slifer the Sky Dragon")
    assert slifer.atk == -1
    assert slifer.def_ == -1

def test_load_and_parse_ygojson_bad_zip(tmp_path):
    """Test that the parser handles BadZipFile gracefully."""
    bad_zip = tmp_path / "bad.zip"
    bad_zip.write_text("Not a zip file")
    
    cards = load_and_parse_ygojson(bad_zip)
    assert cards == []

def test_load_and_parse_ygojson_bad_json(tmp_path):
    """Test that the parser handles JSONDecodeError gracefully."""
    zip_path = tmp_path / "bad_json.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("cards.json", "{ malformed json ]")
        
    cards = load_and_parse_ygojson(zip_path)
    assert cards == []

def test_load_and_parse_ygojson_dict_no_data(tmp_path):
    """Test that the parser handles a dict without 'data' key without crashing."""
    zip_path = tmp_path / "no_data.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        # A dictionary that doesn't have "data"
        zf.writestr("cards.json", json.dumps({"meta": {"date": "today"}}))
        
    cards = load_and_parse_ygojson(zip_path)
    assert cards == []
