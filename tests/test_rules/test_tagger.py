import time
from ygo_ultime_deck.models.card import CardModel, TaggedCardModel
from ygo_ultime_deck.rules.tagger import RegexTagger

def test_tagged_card_model():
    card = TaggedCardModel(
        id="123",
        name="Test Card",
        type="Effect Monster",
        desc="A test description.",
        tags=["Searcher"]
    )
    assert "Searcher" in card.tags
    assert card.name == "Test Card"

def test_regex_tagger_basic_match():
    card = CardModel(
        id="456",
        name="Reinforcement of the Army",
        type="Spell Card",
        desc="Add 1 Level 4 or lower Warrior monster from your Deck to your hand."
    )
    
    rules = {
        "Searcher": r"Add .* from your Deck to your hand"
    }
    
    tagger = RegexTagger(rules)
    tagged_card = tagger.tag_card(card)
    
    assert isinstance(tagged_card, TaggedCardModel)
    assert "Searcher" in tagged_card.tags
    assert tagged_card.id == card.id

def test_regex_tagger_no_match():
    card = CardModel(
        id="789",
        name="Dark Magician",
        type="Normal Monster",
        desc="The ultimate wizard in terms of attack and defense."
    )
    
    rules = {
        "Searcher": r"Add .* from your Deck to your hand"
    }
    
    tagger = RegexTagger(rules)
    tagged_card = tagger.tag_card(card)
    
    assert isinstance(tagged_card, TaggedCardModel)
    assert len(tagged_card.tags) == 0

def test_regex_tagger_multiple_matches():
    card = CardModel(
        id="101",
        name="Combo Card",
        type="Effect Monster",
        desc="Special Summon this card. Add 1 card from your Deck to your hand."
    )
    
    rules = {
        "Searcher": r"Add .* from your Deck to your hand",
        "Extender": r"Special Summon this card"
    }
    
    tagger = RegexTagger(rules)
    tagged_card = tagger.tag_card(card)
    
    assert "Searcher" in tagged_card.tags
    assert "Extender" in tagged_card.tags
    assert len(tagged_card.tags) == 2

def test_regex_tagger_complex_text_no_crash():
    card = CardModel(
        id="102",
        name="Very Long Text Card",
        type="Effect Monster",
        desc="A" * 10000  # Extremely long text to test regex performance/crash
    )
    
    rules = {
        "Searcher": r"Add .* from your Deck to your hand"
    }
    
    tagger = RegexTagger(rules)
    tagged_card = tagger.tag_card(card)
    assert len(tagged_card.tags) == 0

def test_regex_tagger_complex_psct():
    # Test multi-line PSCT parsing with re.DOTALL
    desc = (
        "If this card is Normal or Special Summoned: You can add 1 'HERO' monster from your Deck to your hand.\n"
        "If this card is sent to the GY: You can Special Summon 1 'Destiny HERO' monster from your GY.\n"
        "You can only use each effect of 'Test HERO' once per turn."
    )
    card = CardModel(
        id="103",
        name="Test HERO",
        type="Effect Monster",
        desc=desc
    )
    
    rules = {
        "Searcher": r"add 1 .* from your Deck to your hand",
        "GY_Revive": r"Special Summon .* from your GY"
    }
    
    # We test case sensitivity. Without (?i), it shouldn't match "add" because of "add". Wait, rule says "add". Text says "add". It should match.
    # Actually, text says "add 1 'HERO'". Rule says "add 1 .* from your Deck to your hand". With DOTALL, it should match.
    tagger = RegexTagger(rules)
    tagged_card = tagger.tag_card(card)
    
    assert "Searcher" in tagged_card.tags
    assert "GY_Revive" in tagged_card.tags

def test_regex_tagger_performance():
    # Programmatic speed validation
    card = CardModel(
        id="104",
        name="Speed Card",
        type="Effect Monster",
        desc="Draw 2 cards."
    )
    rules = {f"Rule_{i}": r"Draw \d+ cards\." for i in range(100)}
    tagger = RegexTagger(rules)
    
    start_time = time.perf_counter()
    for _ in range(100):
        tagger.tag_card(card)
    duration = time.perf_counter() - start_time
    
    # Assert that 100 cards against 100 rules takes less than 2.0s to avoid flakiness
    assert duration < 2.0, f"Tagger is too slow: {duration}s"

def test_regex_tagger_duplicate_prevention():
    card = CardModel(
        id="999",
        name="Dup Card",
        type="Effect Monster",
        desc="Search. Search."
    )
    rules = {
        "Searcher": r"Search"
    }
    tagger = RegexTagger(rules)
    tagged_card = tagger.tag_card(card)
    
    # Assert tag is present only once
    assert tagged_card.tags.count("Searcher") == 1

def test_regex_tagger_fields_preservation():
    # Assert that original fields are preserved
    card = CardModel(
        id="105",
        name="Field Preserver",
        type="Effect Monster",
        desc="Preserve.",
        atk=2000,
        def_=1500,
        level=4,
        race="Warrior",
        attribute="EARTH"
    )
    tagger = RegexTagger({})
    tagged_card = tagger.tag_card(card)
    
    assert tagged_card.atk == 2000
    assert getattr(tagged_card, 'def_') == 1500
    assert tagged_card.level == 4
    assert tagged_card.race == "Warrior"
    assert tagged_card.attribute == "EARTH"
