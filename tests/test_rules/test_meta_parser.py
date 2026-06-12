import pytest
from pathlib import Path
from typer import Exit
from ygo_ultime_deck.rules.meta_parser import load_meta_targets

def test_load_meta_targets_valid(tmp_path):
    yaml_file = tmp_path / "meta_targets.yaml"
    content = """
threats:
  - name: "Ash Blossom"
    category: "Handtrap"
    count: 3
"""
    yaml_file.write_text(content, encoding="utf-8")
    
    result = load_meta_targets(yaml_file)
    assert len(result.threats) == 1
    assert result.threats[0].name == "Ash Blossom"
    assert result.threats[0].category == "Handtrap"
    assert result.threats[0].count == 3

def test_load_meta_targets_creates_default(tmp_path):
    yaml_file = tmp_path / "meta_targets_default.yaml"
    assert not yaml_file.exists()
    
    result = load_meta_targets(yaml_file)
    assert yaml_file.exists()
    assert len(result.threats) > 0

def test_load_meta_targets_invalid_yaml(tmp_path):
    yaml_file = tmp_path / "meta_targets_invalid.yaml"
    yaml_file.write_text("invalid: yaml: :", encoding="utf-8")
    
    with pytest.raises(Exit) as exc_info:
        load_meta_targets(yaml_file)
    assert exc_info.value.exit_code == 1

def test_load_meta_targets_validation_error(tmp_path):
    yaml_file = tmp_path / "meta_targets_bad_schema.yaml"
    # Missing required 'name' in threat
    content = """
threats:
  - count: 3
"""
    yaml_file.write_text(content, encoding="utf-8")
    
    with pytest.raises(Exit) as exc_info:
        load_meta_targets(yaml_file)
    assert exc_info.value.exit_code == 1

def test_load_meta_targets_forbid_extra(tmp_path):
    yaml_file = tmp_path / "meta_targets_extra.yaml"
    # Extra field 'invalid_field'
    content = """
threats:
  - name: "Ash Blossom"
    invalid_field: "This should fail"
"""
    yaml_file.write_text(content, encoding="utf-8")
    
    with pytest.raises(Exit) as exc_info:
        load_meta_targets(yaml_file)
    assert exc_info.value.exit_code == 1

def test_load_meta_targets_list_root(tmp_path):
    yaml_file = tmp_path / "meta_targets_list.yaml"
    content = """
- name: "Nibiru"
  category: "Handtrap"
  count: 1
"""
    yaml_file.write_text(content, encoding="utf-8")
    
    result = load_meta_targets(yaml_file)
    assert len(result.threats) == 1
    assert result.threats[0].name == "Nibiru"

def test_load_meta_targets_empty_file(tmp_path):
    yaml_file = tmp_path / "meta_targets_empty.yaml"
    yaml_file.write_text("# just a comment\n", encoding="utf-8")
    
    with pytest.raises(Exit) as exc_info:
        load_meta_targets(yaml_file)
    assert exc_info.value.exit_code == 1

def test_load_meta_targets_os_error(tmp_path):
    dir_path = tmp_path / "a_directory"
    dir_path.mkdir()
    
    with pytest.raises(Exit) as exc_info:
        load_meta_targets(dir_path)
    assert exc_info.value.exit_code == 1

def test_load_meta_targets_unicode_error(tmp_path):
    yaml_file = tmp_path / "meta_targets_unicode.yaml"
    yaml_file.write_bytes(b"\xff\xfe\x00\x00\x80\x00")
    
    with pytest.raises(Exit) as exc_info:
        load_meta_targets(yaml_file)
    assert exc_info.value.exit_code == 1
