import pytest
import pickle
from pydantic import ValidationError
from ygo_ultime_deck.models.card import CardModel, CardRace, CardAttribute

@pytest.fixture
def dark_magician_data():
    return {
        "id": "46986414",
        "name": "Dark Magician",
        "type": "Normal Monster",
        "desc": "The ultimate wizard in terms of attack and defense.",
        "race": "Spellcaster",
        "atk": 2500,
        "def": 2100,
        "level": 7,
        "attribute": "DARK"
    }

@pytest.fixture
def pot_of_greed_data():
    return {
        "id": "55144522",
        "name": "Pot of Greed",
        "type": "Spell Card",
        "desc": "Draw 2 cards.",
        "race": "Normal"
    }

def test_card_instantiation_with_alias(dark_magician_data):
    card = CardModel.model_validate(dark_magician_data)
    assert card.id == "46986414"
    assert card.name == "Dark Magician"
    assert card.card_type == "Normal Monster"
    assert card.desc == "The ultimate wizard in terms of attack and defense."
    assert card.atk == 2500
    assert card.def_ == 2100
    assert card.race == CardRace.SPELLCASTER
    assert card.attribute == CardAttribute.DARK
    
def test_card_optional_fields(pot_of_greed_data):
    card = CardModel.model_validate(pot_of_greed_data)
    assert card.name == "Pot of Greed"
    assert card.atk is None
    assert card.level is None
    assert card.series is None

def test_card_is_picklable(dark_magician_data):
    card = CardModel.model_validate(dark_magician_data)
    pickled_card = pickle.dumps(card)
    unpickled_card = pickle.loads(pickled_card)
    
    assert unpickled_card.id == card.id
    assert unpickled_card.name == card.name
    assert unpickled_card.card_type == card.card_type
    assert unpickled_card.atk == card.atk
    assert unpickled_card.def_ == card.def_
    assert unpickled_card.desc == card.desc
    assert unpickled_card.race == card.race
    assert unpickled_card.attribute == card.attribute

def test_missing_mandatory_fields():
    with pytest.raises(ValidationError) as exc_info:
        CardModel.model_validate({"name": "No ID Card"})
    assert "id" in str(exc_info.value)
    assert "type" in str(exc_info.value)
    assert "desc" in str(exc_info.value)

def test_question_mark_stats():
    slifer_data = {
        "id": "10000020",
        "name": "Slifer the Sky Dragon",
        "type": "Effect Monster",
        "desc": "Gains 1000 ATK/DEF for each card in your hand.",
        "race": "Divine-Beast",
        "atk": "?",
        "def": "?",
        "level": 10,
        "attribute": "DIVINE"
    }
    card = CardModel.model_validate(slifer_data)
    assert card.atk == -1
    assert card.def_ == -1

def test_linkmarkers():
    decode_talker_data = {
        "id": "01861629",
        "name": "Decode Talker",
        "type": "Link Monster",
        "desc": "2+ Effect Monsters",
        "race": "Cyberse",
        "atk": 2300,
        "linkval": 3,
        "linkmarkers": ["Top", "Bottom-Left", "Bottom-Right"],
        "attribute": "DARK"
    }
    card = CardModel.model_validate(decode_talker_data)
    assert card.linkmarkers == ["Top", "Bottom-Left", "Bottom-Right"]
    assert card.linkval == 3
