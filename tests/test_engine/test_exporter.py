import os
import pytest
from ygo_ultime_deck.engine.exporter import generate_ydk

def test_generate_ydk(tmp_path):
    # Setup data
    decklist = {
        "main": [111, 222, 333],
        "extra": [444],
        "side": [555, 666]
    }
    
    filepath = tmp_path / "test_deck.ydk"
    
    # Execution
    generate_ydk(decklist, str(filepath))
    
    # Verification
    assert os.path.exists(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    expected_content = """#created by YGO Ultime Deck
#main
111
222
333
#extra
444
!side
555
666
"""
    assert content == expected_content

def test_generate_ydk_missing_sections(tmp_path):
    # Setup data with missing extra and side
    decklist = {
        "main": [111]
    }
    
    filepath = tmp_path / "test_deck_partial.ydk"
    
    # Execution
    generate_ydk(decklist, str(filepath))
    
    # Verification
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    expected_content = """#created by YGO Ultime Deck
#main
111
#extra
!side
"""
    assert content == expected_content

def test_generate_ydk_creates_directory(tmp_path):
    # Setup path in nested non-existent directory
    decklist = {"main": [1]}
    filepath = tmp_path / "nested" / "dir" / "deck.ydk"
    
    # Execution
    generate_ydk(decklist, str(filepath))
    
    # Verification
    assert os.path.exists(filepath)
