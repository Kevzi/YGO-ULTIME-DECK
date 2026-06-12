## Deferred from: code review of 1-1-initialisation-du-projet-socle-cli-typer.md (2026-06-11)
- Meaningless Test Suite: test_cli.py only tests if the --help command returns an exit code of 0.
- Absence of Static Type Checking: No configuration or developer dependency for static type checking (e.g., mypy, pyright).
- Missing License: Repository lacks a LICENSE file.

## Deferred from: code review of 1-3-telechargeur-ygojson-gestion-du-cache (2026-06-11)
- Hardcoded API Versioning: `DEFAULT_URL` in `downloader.py` explicitly bakes in `v0.6.0`, which might break when the API updates, though intentional for now.

## Deferred from: code review of 1-4-parseur-resilient-pre-filtrage-memoire (2026-06-11)
- Memory Bloat in Parser: Using json.load(f) loads the entire file into memory. Should use an iterative parser.
- Inadequate Field Validation: Missing cross-field validation for normal monsters having Link Value or Pendulum Scale.
- Naive Stat Handling: Only handles the exact string "?", failing on other non-integer string representations.
- Swallowed Exceptions in CLI: The CLI catches Exception and prints a message but suppresses the stack trace, hindering debugging.
## Deferred from: code review (2026-06-11)

- [x] [Review][Defer] Data Destruction (extra="ignore") [src/ygo_ultime_deck/models/card.py:155]   deferred, pre-existing

- [x] [Review][Defer] ReDoS / Backtracking Mitigation   deferred: Architecture Offline-First, règles internes sécurisées.


## Deferred from: code review of 2-2-fichier-de-configuration-externe-tags-rules-yaml.md (2026-06-11)
- [x] [Review][Defer] Inconsistent Localization   deferred, pre-existing
- [x] [Review][Defer] Global State Side-Effects (Console)   deferred, pre-existing
- [x] [Review][Defer] Missing Formal Schema Validation (Pydantic)   deferred, pre-existing



## Deferred from: code review of 2-3-implementation-du-multi-tagging-dynamique.md (2026-06-11)
- Catastrophic Backtracking Vulnerability — re.DOTALL globally with .* creates ReDoS vulnerability.
- Crude Substring Type Checking — "Normal" in card.card_type is fragile.
- Inadequate Regex Stress Testing — test_regex_tagger_complex_text_no_crash does not actually stress the engine.
## Deferred from: code review of 3-1-algorithme-hypergeometrique-logarithmique.md (2026-06-11)
- Corrupted Model Construction via Alias Mismatch
- Catastrophic Global Exception Handler
- Hardcoded Cache Paths
- Aggressive Banlist Pruning
- Suicidal 30s Timeout
- Brittle Schema Definitions
- Silent Failures on Corrupted Cache
- Silent Data Loss on Schema Evolution
- Reckless Directory Traversal
- OOM Vulnerability
- Flawed Progress Bar
- Inefficient Regex Execution Loop
- Unhandled Zip/OS Error
- Unhandled UnicodeDecodeError
- Unhandled Directory Error
- Unhandled YAML UnicodeDecodeError


## Deferred from: code review of 3-2-parseur-des-mains-de-reve-target-combos-yaml.md (2026-06-12)
- Ambiguous `name` field design for cards vs tags (engine might handle resolution later) [`src/ygo_ultime_deck/models/simulation.py`]
- Negative constraints impossible (`count >= 1` limits excluding cards) [`src/ygo_ultime_deck/models/simulation.py`]
- Missing transmission of parameters to math engine (wiring to be done in 3.3) [`src/ygo_ultime_deck/engine/config_parser.py`]
