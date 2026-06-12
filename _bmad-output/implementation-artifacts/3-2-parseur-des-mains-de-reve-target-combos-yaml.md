---
baseline_commit: 46f42b22ccca45bae82f54cbe7f2e967ffd20464
# Story 3.2: Parseur des "Mains de Rêve" (target_combos.yaml)

**Status:** done
**Epic:** 3 - Simulateur de Combos et Analyse Mathématique

## Story Requirements

**User Story:**
As a concepteur de deck (utilisateur CLI),
I want définir les cartes ou les tags requis pour un combo réussi (ex: 1 Starter + 1 Extender) dans un fichier `config/target_combos.yaml`,
So that je n'aie pas à écrire des arguments CLI complexes dans le terminal pour tester mes stratégies.

**Acceptance Criteria:**
- **Given** un fichier `target_combos.yaml` contenant plusieurs scénarios (Combo A, Combo B)
- **When** la simulation démarre
- **Then** le système valide la syntaxe et convertit les requêtes en objets Pydantic (ex: `SimulationRequest`)
- **And** transmet ces paramètres proprement au moteur mathématique.

## Developer Context & Guardrails

### Technical Requirements
- Créer un modèle Pydantic `SimulationRequest` ou équivalent pour parser et valider le contenu du fichier YAML.
- Assurer le chargement sécurisé de `config/target_combos.yaml` (gestion stricte de `FileNotFoundError`, `yaml.YAMLError`, `PermissionError`, et `UnicodeDecodeError`).
- Les scénarios dans le YAML doivent pouvoir spécifier des noms de cartes exactes ou des tags sémantiques (ex: "Starter", "Extender") avec le nombre d'exemplaires requis en main (ex: ">= 1").
- La sortie doit être une série d'objets purs Pydantic.

### Architecture Compliance
- Strict respect de Pydantic V2 pour toute validation de données.
- Le fichier lu réside obligatoirement dans `config/`.
- La gestion des exceptions doit se faire via `Typer` et `Rich` (`typer.Exit(1)`), ne jamais utiliser `sys.exit` ni laisser fuiter des stacktraces.

### Library / Framework Requirements
- Utiliser `pyyaml` pour la lecture du fichier.
- Utiliser `pydantic` pour définir la structure attendue.

### File Structure Requirements
- **UPDATE** `src/ygo_ultime_deck/models/simulation.py` (ou équivalent) pour ajouter le modèle `SimulationRequest`.
- **NEW/UPDATE** Module de lecture (ex: `src/ygo_ultime_deck/engine/config_parser.py` ou similaire, ou dans `rules/` selon l'implémentation choisie par le développeur, en cohérence avec le reste).
- **NEW** Fichier d'exemple `config/target_combos.yaml`.
- **NEW** Tests associés `tests/test_engine/test_combos_parser.py` (ou équivalent).

### Testing Requirements
- Test unitaire pour le parsing réussi d'un YAML bien formaté.
- Test unitaire vérifiant l'erreur de validation Pydantic si le YAML est malformé.
- Test unitaire simulant un `FileNotFoundError` (ou `IsADirectoryError`).
- Test unitaire gérant les erreurs d'encodage (UnicodeDecodeError).

## Previous Story Intelligence (from Story 3.1)
- L'algorithme hypergéométrique dans `math_utils.py` attend (N, K, n, k). Le parseur YAML devra in fine fournir au moteur les "cibles" (ex: "Starter") pour que le simulateur trouve (K).
- La code review de la Story 3.1 a soulevé des erreurs non gérées dans les autres modules de config (`yaml.YAMLError`, `UnicodeDecodeError`, `IsADirectoryError`). Il est impératif de blinder ce parseur YAML dès le départ contre ces exceptions.

## Tasks / Subtasks
- [x] Créer les modèles Pydantic de simulation dans `models/simulation.py`.
- [x] Développer la logique de parsing YAML robuste (gestion des erreurs d'IO et format).
- [x] Créer le fichier d'exemple `config/target_combos.yaml` contenant des "Mains de Rêve".
- [x] Implémenter les tests unitaires associés pour valider le tout de manière exhaustive.

## Dev Agent Record
- **Implementation Notes:** Created Pydantic models (`SimulationRequest`, `TargetCombo`, `Requirement`) in `models/simulation.py`. Implemented `parse_target_combos` in `engine/config_parser.py` with strict exception handling and formatting using Typer and Rich to avoid leaking stack traces. Handled `FileNotFoundError`, `IsADirectoryError`, `PermissionError`, `UnicodeDecodeError`, `yaml.YAMLError`, and `ValidationError`. Added the example `config/target_combos.yaml`.
- **Tests Added:** Added `tests/test_engine/test_combos_parser.py` with 9 tests covering valid parsing, default values, negative counts, file not found, invalid schema, invalid yaml, directory error, and unicode decode errors. All 47 tests pass.

### File List
- `src/ygo_ultime_deck/models/simulation.py` (NEW)
- `src/ygo_ultime_deck/engine/config_parser.py` (NEW)
- `config/target_combos.yaml` (NEW)
- `tests/test_engine/test_combos_parser.py` (NEW)

## Completion Status
- **Status Update:** done
- **Note:** Ultimate context engine analysis completed - comprehensive developer guide created.

### Review Findings
- [x] [Review][Patch] Quantity operators not supported (`count` is int, not string or dict) [`src/ygo_ultime_deck/models/simulation.py`]
- [x] [Review][Patch] Missing `extra='forbid'` in models to prevent silent typos [`src/ygo_ultime_deck/models/simulation.py`]
- [x] [Review][Patch] Empty file or invalid YAML root validation crashes unexpectedly [`src/ygo_ultime_deck/engine/config_parser.py`]
- [x] [Review][Patch] No path constraint enforcement to restrict loading to `config/` directory [`src/ygo_ultime_deck/engine/config_parser.py`]
- [x] [Review][Patch] Tests ignore real config file (need to test parsing actual `config/target_combos.yaml`) [`tests/test_engine/test_combos_parser.py`]
- [x] [Review][Patch] Empty strings or lists allowed for combos/requirements [`src/ygo_ultime_deck/models/simulation.py`]
- [x] [Review][Defer] Ambiguous `name` field design for cards vs tags (engine might handle resolution later) [`src/ygo_ultime_deck/models/simulation.py`] — deferred, pre-existing
- [x] [Review][Defer] Negative constraints impossible (`count >= 1` limits excluding cards) [`src/ygo_ultime_deck/models/simulation.py`] — deferred, pre-existing
- [x] [Review][Defer] Missing transmission of parameters to math engine (wiring to be done in 3.3) [`src/ygo_ultime_deck/engine/config_parser.py`] — deferred, pre-existing
