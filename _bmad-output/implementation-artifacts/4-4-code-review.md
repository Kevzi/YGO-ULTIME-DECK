# Code Review Findings: Story 4.4

## Acceptance Criteria Audits
- **[AI-Review][High] Mock IDs instead of Official IDs:** The `audit` command hardcodes dummy card IDs in the export (`[11111111] * opt_size` for main deck). The exported `.ydk` will not contain actual official IDs as requested. *Fix: Extract real IDs from target combos or pass valid realistic mock IDs based on actual config.*
- **[AI-Review][Medium] File Structure Deviation:** The new CLI command was integrated into `src/ygo_ultime_deck/main.py` instead of creating `cli.py`. *Fix: Rename main.py to cli.py or update the spec file to reflect this.*
- **[AI-Review][High] Ignored Core Parameter:** The CLI accepts a `--core` parameter but ignores it when constructing the mock deck for simulation (`["Extender"] * 3 + ["Brick"] * ...`). *Fix: Use the `--core` parameter properly.*

## Edge Case & Adversarial Findings
- **[AI-Review][High] `os.makedirs` FileNotFoundError:** If `filepath` contains no directory separators (e.g., `--output deck.ydk`), `os.path.dirname(filepath)` returns `""`, which causes `os.makedirs("", exist_ok=True)` to crash on Windows. *Fix: Use `pathlib` or check `if dir_path`.*
- **[AI-Review][High] Silent Failure on Configuration Parsing:** If `target_combos.yaml` is invalid, the `except Exception` block silently swallows the error and skips the simulation without notifying the user. *Fix: Show the error.*
- **[AI-Review][High] Dangerous Deck Truncation Risk:** `opt_size` could be smaller than `starters + garnets + 3` if the user puts crazy inputs, resulting in a mock deck that blindly slices off essential `Extender` or `Garnet` cards. *Fix: Ensure mock deck is properly bounded.*
- **[AI-Review][High] ZeroDivisionError Risk:** If `iterations=0`, `rate = (successes / sim_result.total_iterations) * 100` will crash. *Fix: Check if total_iterations > 0.*
- **[AI-Review][Medium] Lying to the User on Error:** When the `.ydk` export fails, the CLI displays the success table and falsely prints `Decklist exportée vers: [path]`. *Fix: Add an `export_success` flag.*
- **[AI-Review][Low] Hardcoded Extra/Side Decks:** The mock export always generates exactly 15 Extra and 15 Side deck cards. *Fix: Pass empty lists or valid ones.*
- **[AI-Review][Low] Inconsistent Filesystem Libraries:** The project utilizes `pathlib.Path` extensively, but `exporter.py` awkwardly reverts to the legacy `os` module. *Fix: Use `pathlib` in `exporter.py`.*

## Conclusion
The YDK generation and CLI integration are well done, but lack some defensive programming for edge cases. Also, the use of Mock IDs breaks the acceptance criteria, even though we don't have a full database integrated yet.
