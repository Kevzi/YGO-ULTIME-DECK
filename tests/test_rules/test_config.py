import pytest
import typer
from pathlib import Path
from ygo_ultime_deck.rules.config import load_tags_rules

def test_load_valid_yaml(tmp_path: Path):
    yaml_file = tmp_path / "tags_rules.yaml"
    yaml_content = """
    Searcher: '(?i)add .* from your deck to your hand'
    Extender: 'Special Summon this card'
    """
    yaml_file.write_text(yaml_content, encoding="utf-8")
    
    rules = load_tags_rules(yaml_file)
    assert isinstance(rules, dict)
    assert "Searcher" in rules
    assert "Extender" in rules
    assert rules["Searcher"] == "(?i)add .* from your deck to your hand"

def test_file_creation_when_not_found(tmp_path: Path):
    non_existent_file = tmp_path / "config" / "does_not_exist.yaml"
    
    # Ensure it doesn't exist initially
    assert not non_existent_file.exists()
    
    # Loading it should create it with defaults
    rules = load_tags_rules(non_existent_file)
    
    assert non_existent_file.exists()
    assert isinstance(rules, dict)
    assert "Starter" in rules
    assert "Extender" in rules

def test_invalid_yaml(tmp_path: Path):
    yaml_file = tmp_path / "tags_rules.yaml"
    # Invalid YAML (missing colon, weird indentation)
    yaml_content = """
    Searcher '(?i)add .* from your deck to your hand'
      Extender: 'Special Summon this card'
    """
    yaml_file.write_text(yaml_content, encoding="utf-8")
    
    with pytest.raises(typer.Exit) as exc_info:
        load_tags_rules(yaml_file)
        
    assert exc_info.value.exit_code == 1

def test_empty_yaml(tmp_path: Path):
    yaml_file = tmp_path / "empty.yaml"
    yaml_file.write_text("", encoding="utf-8")
    
    with pytest.raises(typer.Exit) as exc_info:
        load_tags_rules(yaml_file)
        
    assert exc_info.value.exit_code == 1

def test_invalid_yaml_schema(tmp_path: Path):
    yaml_file = tmp_path / "invalid_schema.yaml"
    yaml_content = """
    - item1
    - item2
    """
    yaml_file.write_text(yaml_content, encoding="utf-8")
    
    with pytest.raises(typer.Exit) as exc_info:
        load_tags_rules(yaml_file)
        
    assert exc_info.value.exit_code == 1

def test_invalid_types_in_dict(tmp_path: Path):
    yaml_file = tmp_path / "invalid_types.yaml"
    yaml_content = """
    Searcher: ['a list instead of a regex string']
    """
    yaml_file.write_text(yaml_content, encoding="utf-8")
    
    with pytest.raises(typer.Exit) as exc_info:
        load_tags_rules(yaml_file)
        
    assert exc_info.value.exit_code == 1

