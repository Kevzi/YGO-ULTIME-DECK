# Code Review Findings: Story 5.2

## Acceptance Criteria Audits
- **[AI-Review][High] Deduplication alters quantities:** Extracting names with `if req.name not in export_names` deduplicates cards. If a combo requires 3 copies of a card, only 1 is exported. *Fix: Append `req.name` `req.count` times.*
- **[AI-Review][Medium] Omission of Unit Tests:** The developer explicitly skipped adding unit tests for the name extraction and padding logic, stating it was covered elsewhere. This violates best practices for testing new data transformation logic. *Fix: Add a test for the `export_names` logic or refactor it into a testable pure function.*
- **[AI-Review][Low] Unconditional execution:** CardResolver initializes even if export isn't needed, though `output` is currently default.
- **[AI-Review][Low] Missed `--core` fallback:** The spec suggested using `--core` as a string fallback, but it was left as an int.

## Edge Case & Adversarial Findings
- **[AI-Review][High] Path Fragility:** `Path(__file__).resolve().parent.parent.parent` is highly fragile and will break if the package structure changes or if installed as a wheel. *Fix: Use a robust path resolution relative to a known config directory or package root.*
- **[AI-Review][Medium] Potential Iteration Crash:** If `request.combos` is None or `combo.requirements` is None, iterating over them will throw a `TypeError`. *Fix: Ensure safe iteration (e.g. `request.combos or []`).*
- **[AI-Review][Medium] O(N^2) Uniqueness Check:** Using `if req.name not in export_names` with a list is inefficient. *Fix: Use a `set` to track seen names while appending to the list.*
- **[AI-Review][Low] Silent Truncation:** `export_names = export_names[:opt_size]` silently drops cards without a warning if the user requested more distinct cards than `opt_size`. *Fix: Add a `logger.warning` if truncation occurs.*
- **[AI-Review][Low] Inline Imports:** `from ygo_ultime_deck.engine.resolver import CardResolver` inside a function violates PEP8. *Fix: Move to the top of the file.*
- **[AI-Review][Low] Untracked Generated Artifacts:** `output/decklist_ultime.ydk` was accidentally tracked in git. *Fix: Add to `.gitignore` and remove from tracking.*

## Conclusion
The integration correctly fulfills the acceptance criteria by fetching names and calling the resolver. However, the data extraction logic inside the CLI command is slightly sloppy (inline imports, O(N^2) list checks, fragile paths, and missing edge-case guards for None values). A quick refactor of this section will make it production-ready.
