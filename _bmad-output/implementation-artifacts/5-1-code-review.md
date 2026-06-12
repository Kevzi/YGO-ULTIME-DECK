# Code Review Findings: Story 5.1

## Acceptance Criteria Audits
- **[AI-Review][Medium] Missing Log Assertion:** The test `test_resolve_invalid_name` does not verify that a warning was actually logged, as required by the testing criteria. *Fix: Use `caplog` to assert the warning.*
- **[AI-Review][Medium] Potential Crash on Invalid Card IDs:** `int(card_id)` can raise `ValueError` or `TypeError` if the API provides non-numeric data, which is not caught and will crash the lazy-loader. *Fix: Wrap in try/except or catch `ValueError`/`TypeError`.*
- **[AI-Review][High] Potential Crash on File I/O:** Opening the zip can raise `OSError` or `PermissionError`, which are not caught by the current `except (zipfile.BadZipFile, json.JSONDecodeError)` block. *Fix: Add `OSError` to the except block.*

## Edge Case & Adversarial Findings
- **[AI-Review][Low] Memory Efficiency:** `json.load()` reads the entire JSON payload at once. While it works for the current size, an iterative JSON parser would be safer against memory bloat. *Fix: Acknowledged, but standard JSON is fine for MVP.*
- **[AI-Review][Low] Missing Encoding Specification:** `zf.open()` returns a byte stream. Feeding bytes directly into `json.load()` is implicit. *Fix: Use `io.TextIOWrapper(f, encoding='utf-8')`.*
- **[AI-Review][Low] Hardcoded Magic Numbers:** The mock ID `11111111` is hardcoded twice. *Fix: Extract to a class-level constant `DEFAULT_MOCK_ID`.*
- **[AI-Review][Medium] Missing Whitespace Sanitization:** The resolver converts names to lowercase but neglects to `.strip()` whitespace. Trailing spaces from raw text inputs will cause silent cache misses. *Fix: Use `.strip().lower()`.*
- **[AI-Review][Medium] Log Spam Potential:** If 40 cards are missing, the resolver spams 40 warnings. *Fix: We will leave as is for now, but good point.*
- **[AI-Review][High] Unsafe Handling of None:** Passing `None` or a single string to `resolve()` will crash or parse incorrectly. *Fix: Add input validation (`if not names: return []`).*

## Conclusion
The `CardResolver` is a great start and perfectly implements the lazy-loading requirement. However, it lacks robustness against I/O errors and dirty string inputs. Fixing these will make it rock solid.
