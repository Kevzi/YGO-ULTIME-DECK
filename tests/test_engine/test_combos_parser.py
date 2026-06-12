import pytest
import typer
import os
from pathlib import Path
from pydantic import ValidationError
from ygo_ultime_deck.models.simulation import SimulationRequest, TargetCombo, Requirement
from ygo_ultime_deck.engine.config_parser import parse_target_combos

def test_simulation_request_valid():
    data = {
        "combos": [
            {
                "name": "Combo A",
                "requirements": [
                    {"name": "Starter", "count": 1},
                    {"name": "Extender", "count": ">= 1"}
                ]
            }
        ]
    }
    req = SimulationRequest(**data)
    assert len(req.combos) == 1
    combo = req.combos[0]
    assert combo.name == "Combo A"
    assert len(combo.requirements) == 2
    assert combo.requirements[0].name == "Starter"
    assert combo.requirements[0].count == 1
    assert combo.requirements[1].count == ">= 1"

def test_simulation_request_default_count():
    data = {
        "combos": [
            {
                "name": "Combo B",
                "requirements": [
                    {"name": "Starter"}
                ]
            }
        ]
    }
    req = SimulationRequest(**data)
    assert req.combos[0].requirements[0].count == 1

def test_simulation_request_extra_forbid():
    data = {
        "combos": [
            {
                "name": "Combo C",
                "requirements": [
                    {"name": "Starter", "coun": 2}
                ]
            }
        ]
    }
    with pytest.raises(ValidationError):
        SimulationRequest(**data)

def test_parse_target_combos_valid(tmp_path):
    # Mocking inside config path to bypass constraint for this test
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    yaml_file = config_dir / "target_combos.yaml"
    yaml_file.write_text('''
combos:
  - name: "Full Combo"
    requirements:
      - name: "Starter"
        count: 1
      - name: "Extender"
        count: 1
''', encoding="utf-8")

    req = parse_target_combos(str(yaml_file))
    assert isinstance(req, SimulationRequest)
    assert len(req.combos) == 1
    assert req.combos[0].name == "Full Combo"
    assert len(req.combos[0].requirements) == 2

def test_parse_target_combos_real_file():
    # Test against the real shipped config
    real_path = Path("config/target_combos.yaml")
    if real_path.exists():
        req = parse_target_combos(str(real_path))
        assert isinstance(req, SimulationRequest)
        assert len(req.combos) > 0

def test_parse_target_combos_not_in_config(tmp_path):
    yaml_file = tmp_path / "target_combos.yaml"
    yaml_file.write_text("combos: []", encoding="utf-8")
    with pytest.raises(typer.Exit):
        parse_target_combos(str(yaml_file))

def test_parse_target_combos_file_not_found():
    with pytest.raises(typer.Exit):
        parse_target_combos("config/non_existent_file.yaml")

def test_parse_target_combos_empty_yaml(tmp_path):
    config_dir = tmp_path / "config"
    config_dir.mkdir(exist_ok=True)
    yaml_file = config_dir / "empty.yaml"
    yaml_file.write_text("", encoding="utf-8")

    with pytest.raises(typer.Exit):
        parse_target_combos(str(yaml_file))

def test_parse_target_combos_invalid_yaml(tmp_path):
    config_dir = tmp_path / "config"
    config_dir.mkdir(exist_ok=True)
    yaml_file = config_dir / "invalid.yaml"
    yaml_file.write_text('''
combos:
  - name: "Full Combo
    requirements: [
''', encoding="utf-8")

    with pytest.raises(typer.Exit):
        parse_target_combos(str(yaml_file))

def test_parse_target_combos_invalid_schema(tmp_path):
    config_dir = tmp_path / "config"
    config_dir.mkdir(exist_ok=True)
    yaml_file = config_dir / "invalid_schema.yaml"
    yaml_file.write_text('''
combos:
  - not_name: "Full Combo"
''', encoding="utf-8")

    with pytest.raises(typer.Exit):
        parse_target_combos(str(yaml_file))

def test_parse_target_combos_is_directory(tmp_path):
    config_dir = tmp_path / "config"
    config_dir.mkdir(exist_ok=True)
    with pytest.raises(typer.Exit):
        parse_target_combos(str(config_dir))

def test_parse_target_combos_unicode_decode_error(tmp_path):
    config_dir = tmp_path / "config"
    config_dir.mkdir(exist_ok=True)
    yaml_file = config_dir / "bad_encoding.yaml"
    yaml_file.write_bytes(b'\xff\xfe\x00\x00')
    
    with pytest.raises(typer.Exit):
        parse_target_combos(str(yaml_file))