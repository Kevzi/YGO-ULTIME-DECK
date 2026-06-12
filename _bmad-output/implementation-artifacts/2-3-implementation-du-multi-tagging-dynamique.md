---
baseline_commit: 46f42b22ccca45bae82f54cbe7f2e967ffd20464
# Story 2.3: Implémentation du Multi-Tagging Dynamique

**Status:** done
**Epic:** 2 - Personnalisation et Auto-Tagging Sémantique

## Story Requirements

**User Story:**
As a simulateur de combos (Moteur Mathématique),
I want que les cartes puissent recevoir une liste de rôles au lieu d'un rôle unique (ex: `[Starter, Extender]`),
So that je puisse tester virtuellement tous ces rôles en fonction des autres cartes en main pour trouver le combo optimal.

**Acceptance Criteria:**
- **Given** une carte dont l'effet match plusieurs règles Regex différentes
- **When** le moteur de tagging a fini son traitement
- **Then** l'attribut `CardModel.tags` contient une liste Python native de tous les tags validés
- **And** la liste ne contient aucun doublon.

## Developer Context & Guardrails

### Technical Requirements
- Vérifier que `RegexTagger.tag_card` retourne bien une liste de tags (`list[str]`) et non un simple booléen ou une chaîne unique.
- S'assurer que le modèle `TaggedCardModel` dans `src/ygo_ultime_deck/models/card.py` déclare bien `tags: list[str] = Field(default_factory=list)`.
- S'assurer que la liste générée ne contient pas de doublons (bien que la structure de dictionnaire de `rules` l'empêche nativement, il faut garantir ce comportement).

### Architecture Compliance
- Le flux de données doit rester inchangé : `CardModel` en entrée, `TaggedCardModel` en sortie sans mutation du modèle d'origine (Pydantic `model_construct` recommandé pour la performance).

### Testing Requirements
- Valider par un test unitaire (dans `tests/test_rules/test_tagger.py`) qu'une carte factice avec un texte combinant "Searcher" et "Extender" reçoit bien les deux tags simultanément.
- (NOTE: Il semble que ce comportement ait déjà été implémenté en avance lors de la Story 2.1. Vérifiez l'existant avant de redévelopper.)

## Previous Story Intelligence
- Dans la Story 2.1 et 2.2, `RegexTagger` et son injection dynamique via `config.py` ont été mis en place.
- La méthode `tag_card` itère déjà sur le dictionnaire de règles.

## Git Intelligence
- Les tests existants incluent peut-être déjà `test_regex_tagger_multiple_matches`.

## Project Context Reference
- Le Multi-Tagging est crucial pour l'Epic 3 (Simulateur de combos). Par exemple, une carte pouvant agir comme Starter ou Extender selon le reste de la main doit posséder les deux identifiants pour que l'algorithme hypergéométrique les comptabilise correctement.

## Tasks / Subtasks
- [x] Vérifier/Implémenter le champ `tags: list[str]` dans `TaggedCardModel`.
- [x] Vérifier/Implémenter la capacité de `RegexTagger.tag_card` à accumuler plusieurs tags.
- [x] S'assurer de l'absence de doublons dans la liste de tags retournée.
- [x] Valider ou écrire les tests unitaires pour le Multi-Tagging.

## Completion Status
- **Status Update:** done
- **Note:** Implementation complete. Already done in story 2.1.

## Dev Agent Record
### Debug Log
- N/A

### Completion Notes
- Verification confirmed that `TaggedCardModel` uses `list[str]` natively.
- `RegexTagger.tag_card` accumulates all matched keys in the `compiled_rules` dictionary. Since dictionary keys are intrinsically unique, duplicates are strictly impossible by Python design.
- The pre-existing test `test_regex_tagger_multiple_matches` inside `tests/test_rules/test_tagger.py` completely covers the requested functionality.
- Therefore, the acceptance criteria are already satisfied without writing new code.

## File List
- `src/ygo_ultime_deck/models/card.py`
- `src/ygo_ultime_deck/rules/tagger.py`
- `tests/test_rules/test_tagger.py`

### Review Findings
- [x] [Review][Patch] Silent Error Swallowing in Rule Compilation — Invalid regex patterns are caught with `pass` and no logging. [src/ygo_ultime_deck/rules/tagger.py:19]
- [x] [Review][Patch] Fragile Path Resolution — `from_config` relies on brittle relative directory traversal. [src/ygo_ultime_deck/rules/tagger.py:39]
- [x] [Review][Patch] Flaky Performance Unit Test — `test_regex_tagger_performance` relies on wall-clock time which is flaky in CI. [tests/test_rules/test_tagger.py:133]
- [x] [Review][Patch] Missing Null Checks for Card Descriptions — `tag_card` passes `card.desc` directly to regex search which will crash if None. [src/ygo_ultime_deck/rules/tagger.py:63]
- [x] [Review][Patch] Type Hint Violation — `filepath: str | None` assigned a `pathlib.Path` object. [src/ygo_ultime_deck/rules/tagger.py:39]
- [x] [Review][Patch] Missing explicit test case for duplicate prevention — Needs a dedicated test asserting duplicates are prevented. [tests/test_rules/test_tagger.py]
- [x] [Review][Defer] Catastrophic Backtracking Vulnerability — `re.DOTALL` globally with `.*` creates ReDoS vulnerability. — deferred, pre-existing
- [x] [Review][Defer] Crude Substring Type Checking — `"Normal" in card.card_type` is fragile. — deferred, pre-existing
- [x] [Review][Defer] Inadequate Regex Stress Testing — `test_regex_tagger_complex_text_no_crash` does not actually stress the engine. — deferred, pre-existing
