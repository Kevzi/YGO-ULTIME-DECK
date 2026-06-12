---
baseline_commit: 46f42b22ccca45bae82f54cbe7f2e967ffd20464
# Story 3.1: Algorithme Hypergéométrique Logarithmique

**Status:** done
**Epic:** 3 - Simulateur de Combos et Analyse Mathématique

## Story Requirements

**User Story:**
As a moteur mathématique,
I want calculer les probabilités de tirage via un algorithme logarithmique (ex: `math.lgamma`),
So that le système ne crashe jamais sur une erreur de dépassement de mémoire ("overflow") lors du calcul de factoriels massifs (ex: factorielle de 60).

**Acceptance Criteria:**
- **Given** un calcul de probabilité complexe sur un deck de 60 cartes
- **When** la fonction `calculate_hypergeometric` est appelée
- **Then** l'algorithme utilise les logarithmes pour neutraliser le risque d'overflow
- **And** retourne la probabilité mathématiquement exacte (float) pour une main statique.

## Developer Context & Guardrails

### Technical Requirements
- Implémenter l'algorithme hypergéométrique en utilisant des mathématiques logarithmiques (la fonction `math.lgamma` en Python est recommandée pour calculer le logarithme continu de `n!`).
- Formule log-binomiale: `log_binom(n, k) = math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)`.
- La fonction doit prendre la taille de la population (N), le nombre de succès dans la population (K), la taille de l'échantillon (n), et le nombre de succès tirés (k).
- S'assurer que le résultat final est re-transformé de l'espace log en probabilité (via `math.exp`).

### Architecture Compliance
- Ne **JAMAIS** utiliser `math.factorial` ou `math.comb` de la bibliothèque standard pour de très grands nombres répétés, car cela entraînerait inévitablement des ralentissements ou des MemoryErrors (OverflowError) sur de grandes échelles (ex: 100 000 itérations), d'où le nom "Logarithmique" de la story.
- Le fichier doit être placé dans le module de calcul: `src/ygo_ultime_deck/engine/math_utils.py`
- L'implémentation doit être une "Pure Function" sans aucun état global.

### File Structure Requirements
- `src/ygo_ultime_deck/engine/__init__.py`
- `src/ygo_ultime_deck/engine/math_utils.py`
- `tests/test_engine/__init__.py`
- `tests/test_engine/test_math_utils.py`

### Testing Requirements
- Ajouter des tests unitaires dans `tests/test_engine/test_math_utils.py`.
- Vérifier des cas connus. Par exemple, pour un deck de 40 (N), avec 3 exemplaires d'une carte (K), et piocher 5 cartes (n), la probabilité d'en obtenir exactement 1 (k) doit être proche d'une valeur connue (~30%).
- Vérifier que les probabilités ne déclenchent pas d'exception sur un deck de 60 cartes avec de très nombreux combos en calcul simultané.

## Tasks / Subtasks
- [x] Créer le module `src/ygo_ultime_deck/engine/` avec `__init__.py`.
- [x] Implémenter la fonction `calculate_hypergeometric` en utilisant `math.lgamma` dans `math_utils.py`.
- [x] Implémenter une fonction utilitaire `log_comb` ou `log_choose` pour structurer le code si nécessaire.
- [x] Créer la suite de tests correspondante dans `tests/test_engine/test_math_utils.py`.
- [x] Valider que la fonction retourne bien des probabilités valides (entre 0.0 et 1.0) et résiste au stress des tests.

### Review Findings
- [x] [Review][Patch] Missing stress test for simultaneous calculations [`tests/test_engine/test_math_utils.py`]
- [x] [Review][Defer] Corrupted Model Construction via Alias Mismatch [`src/ygo_ultime_deck/rules/tagger.py`] — deferred, pre-existing
- [x] [Review][Defer] Catastrophic Global Exception Handler [`src/ygo_ultime_deck/main.py`] — deferred, pre-existing
- [x] [Review][Defer] Hardcoded Cache Paths [`src/ygo_ultime_deck/main.py`] — deferred, pre-existing
- [x] [Review][Defer] Aggressive Banlist Pruning [`src/ygo_ultime_deck/ingestion/parser.py`] — deferred, pre-existing
- [x] [Review][Defer] Suicidal 30s Timeout [`src/ygo_ultime_deck/ingestion/downloader.py`] — deferred, pre-existing
- [x] [Review][Defer] Brittle Schema Definitions [`src/ygo_ultime_deck/models/card.py`] — deferred, pre-existing
- [x] [Review][Defer] Silent Failures on Corrupted Cache [`src/ygo_ultime_deck/ingestion/parser.py`] — deferred, pre-existing
- [x] [Review][Defer] Silent Data Loss on Schema Evolution [`src/ygo_ultime_deck/ingestion/parser.py`] — deferred, pre-existing
- [x] [Review][Defer] Reckless Directory Traversal [`src/ygo_ultime_deck/rules/tagger.py`] — deferred, pre-existing
- [x] [Review][Defer] OOM Vulnerability [`src/ygo_ultime_deck/ingestion/parser.py`] — deferred, pre-existing
- [x] [Review][Defer] Flawed Progress Bar [`src/ygo_ultime_deck/ingestion/downloader.py`] — deferred, pre-existing
- [x] [Review][Defer] Inefficient Regex Execution Loop [`src/ygo_ultime_deck/rules/tagger.py`] — deferred, pre-existing
- [x] [Review][Defer] Unhandled Zip/OS Error [`src/ygo_ultime_deck/ingestion/parser.py`] — deferred, pre-existing
- [x] [Review][Defer] Unhandled UnicodeDecodeError [`src/ygo_ultime_deck/ingestion/parser.py`] — deferred, pre-existing
- [x] [Review][Defer] Unhandled Directory Error [`src/ygo_ultime_deck/rules/config.py`] — deferred, pre-existing
- [x] [Review][Defer] Unhandled YAML UnicodeDecodeError [`src/ygo_ultime_deck/rules/config.py`] — deferred, pre-existing

## Dev Agent Record
- **Implementation Notes:** Created `engine` module with `math_utils.py`. Implemented `log_binom` using `math.lgamma` to prevent factorial overflow. Implemented `calculate_hypergeometric` combining logarithmic binomials. Handled edge cases (impossible events, bounded probabilities to 0.0-1.0).
- **Tests Added:** `test_math_utils.py` checks known cases, boundary values, and verifies 0 memory errors on extreme sample sizes like N=1000.
- **Completion Summary:** The core hypergeometric engine is successfully created and shielded from memory overflows, fulfilling FR7 and NFR3.
- **Change Log:**
  - Added `src/ygo_ultime_deck/engine/__init__.py`
  - Added `src/ygo_ultime_deck/engine/math_utils.py`
  - Added `tests/test_engine/__init__.py`
  - Added `tests/test_engine/test_math_utils.py`

## Completion Status
- **Status Update:** done
- **Note:** Ultimate context engine analysis completed - comprehensive developer guide created.
