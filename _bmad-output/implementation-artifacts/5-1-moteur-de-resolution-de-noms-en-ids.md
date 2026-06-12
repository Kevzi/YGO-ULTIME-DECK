---
baseline_commit: 3bd579ec4bd2fbdbb96bcbe431f058200973b308
# Story 5.1: Moteur de résolution de noms en IDs

**Status:** ready-for-dev
**Epic:** 5 - Base de Données Cartes et Résolution d'IDs

## Story Requirements

**User Story:**
As a moteur d'exportation YDK,
I want pouvoir résoudre un nom de carte en son ID officiel en consultant la base de données locale (SQLite/YGOJSON),
So that la "Decklist Ultime" générée soit composée de vrais IDs valides importables dans Omega ou Edopro.

**Acceptance Criteria:**
- **Given** une liste de noms de cartes configurées dans la simulation
- **When** le moteur de résolution est appelé
- **Then** il effectue une recherche efficace dans la base de données `data/cache/aggregate.zip` ou via un cache SQLite
- **And** retourne une liste d'entiers (les IDs officiels des cartes correspondantes)
- **And** gère les cas d'erreur où le nom de la carte n'est pas trouvé (log warning, fallback mock id).

## Developer Context & Guardrails

### Technical Requirements
- Le fichier `aggregate.zip` téléchargé à l'Epic 1.3 contient toutes les données JSON.
- Créer un module `src/ygo_ultime_deck/engine/resolver.py`.
- Il doit être capable de charger le JSON et de construire un dictionnaire `nom -> id` en mémoire (ou utiliser SQLite si besoin de perfs).
- Le dictionnaire doit être "lazy-loaded" (chargé uniquement au moment de l'export) pour ne pas ralentir l'audit global si on n'exporte pas le YDK.
- Si le nom d'une carte n'est pas trouvé, retourner un Mock ID et logger un avertissement sans planter l'export.

### Architecture Compliance
- Ne pas casser la vitesse de la CLI.
- Le nom doit être cherché en version "case-insensitive".

### File Structure Requirements
- **NEW** `src/ygo_ultime_deck/engine/resolver.py` : Logique de résolution.
- **NEW** `tests/test_engine/test_resolver.py` : Tests unitaires associés.

### Testing Requirements
- Test d'une résolution valide (ex: "Ash Blossom & Joyous Spring" -> 14558127).
- Test d'une résolution invalide (ex: "Carte Inexistante" -> Warning + Mock ID).
- Test d'optimisation de cache (vérifier que le chargement ne se fait qu'une fois).

## Tasks / Subtasks
- [x] Créer `Resolver` classe ou fonction lazy-loading.
- [x] Intégrer l'ouverture du `aggregate.zip`.
- [x] Ajouter la gestion des erreurs et avertissements.
- [x] Créer les tests unitaires.

## Dev Agent Record
- **Implementation Notes:** J'ai implémenté la classe `CardResolver` qui prend le chemin vers `aggregate.zip`. Elle s'initialise rapidement et retarde la lecture du zip et le parsing JSON jusqu'au premier appel de la méthode `resolve()`. Le dictionnaire généré permet une complexité O(1) pour résoudre une infinité de noms.
- **Tests Added:** `tests/test_engine/test_resolver.py` avec 4 tests : valid names (insensible à la casse), invalid names (fallback mock id 11111111), missing zip file (robustesse sans crash), et lazy loading (vérification du chargement unique).

### File List
- `src/ygo_ultime_deck/engine/resolver.py`
- `tests/test_engine/test_resolver.py`

## Change Log
- Ajout de `src/ygo_ultime_deck/engine/resolver.py` contenant `CardResolver`
- Ajout de `tests/test_engine/test_resolver.py`

## Completion Status
- **Status Update:** done
- **Note:** Initial story definition completed.

## Code Review Findings
**Severity Breakdown:** 2 High | 4 Medium | 3 Low

### Action Items
- [x] [AI-Review][Medium] Missing Log Assertion: Add `caplog` to `test_resolve_invalid_name`.
- [x] [AI-Review][Medium] Potential Crash on Invalid Card IDs: Catch `ValueError`/`TypeError` when calling `int()`.
- [x] [AI-Review][High] Potential Crash on File I/O: Add `OSError` to the zipfile exception block.
- [x] [AI-Review][Low] Missing Encoding Specification: Use `io.TextIOWrapper(f, encoding='utf-8')`.
- [x] [AI-Review][Low] Hardcoded Magic Numbers: Extract `11111111` to `DEFAULT_MOCK_ID`.
- [x] [AI-Review][Medium] Missing Whitespace Sanitization: Use `.strip().lower()`.
- [x] [AI-Review][High] Unsafe Handling of None: Add type check / guard clause for `names`.
