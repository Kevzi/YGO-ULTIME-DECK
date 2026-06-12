---
baseline_commit: d98d8eec0716809ece00e8c3f3ce86f1bbe1c839
# Story 4.1: Parseur des Menaces de la Méta (`meta_targets.yaml`)

**Status:** ready-for-dev
**Epic:** 4 - Génération de la "Decklist Ultime" et Exportation YDK

## Story Requirements

**User Story:**
As a utilisateur CLI,
I want définir les "staples" (cartes génériques jouées par l'adversaire) et les decks méta dans un fichier `config/meta_targets.yaml`,
So that le système connaisse les interruptions majeures contre lesquelles il doit tester l'immunité de mes combos.

**Acceptance Criteria:**
- **Given** un fichier `config/meta_targets.yaml` contenant des menaces comme "Ash Blossom" ou "Nibiru"
- **When** l'analyse de méta démarre
- **Then** l'outil parse ces menaces et prépare une liste d'interruptions virtuelles (sous forme de modèles Pydantic)
- **And** gère les cas où le fichier est manquant ou mal formaté avec un message d'erreur clair.

## Developer Context & Guardrails

### Technical Requirements
- Créer un modèle Pydantic dans `models/meta.py` (ou ajouter à un fichier pertinent existant) pour représenter une Menace / Interruption (ex: `MetaThreat` avec un nom, une catégorie de type de carte, etc.).
- Créer un module de parsing robuste qui charge `config/meta_targets.yaml` en utilisant PyYAML et valide le contenu avec le modèle Pydantic.
- Le fichier YAML devrait suivre une structure simple, par exemple une liste d'objets ou un dictionnaire de catégories (Handtraps, Board Breakers). Pour une V1, une simple liste de noms ou objets suffira.
- S'inspirer fortement du pattern implémenté dans `rules/config.py` ou le parseur de `target_combos.yaml`.

### Architecture Compliance
- Utiliser **Pydantic** (`ConfigDict(extra='forbid')`) pour s'assurer que le fichier YAML ne contient pas de champs fantômes.
- Le parseur doit utiliser `typer.Exit(1)` (via `rich.console`) si le fichier est corrompu.
- Penser à créer le fichier YAML par défaut s'il n'existe pas, avec des exemples classiques (Ash Blossom, Infinite Impermanence, Nibiru).

### File Structure Requirements
- **NEW** `src/ygo_ultime_deck/models/meta.py` : Pydantic models (ex: `MetaThreat`, `MetaTargetsRequest`).
- **NEW** `src/ygo_ultime_deck/rules/meta_parser.py` (ou équivalent) : Logique de parsing.
- **NEW** `tests/test_rules/test_meta_parser.py` : Tests unitaires.

### Testing Requirements
- Test de chargement d'un fichier YAML valide.
- Test de rejet d'un fichier YAML contenant des champs invalides (ValidationError de Pydantic).
- Test de création automatique du fichier par défaut si le fichier cible n'existe pas.

## Previous Story Intelligence (from Epic 3)
- Le parseur de l'Epic 3 a validé l'approche "modèles Pydantic stricts" + "messages d'erreurs clairs via Rich".
- Il est crucial de séparer la logique de parsing (Lecture de fichier + validation Pydantic) du moteur d'exécution (Epic 4, Story 4.2). Cette Story 4.1 ne s'occupe QUE de la lecture et de la validation des données en mémoire.

## Tasks / Subtasks
- [x] Créer les modèles Pydantic pour les menaces (`MetaThreat`).
- [x] Écrire la fonction de parsing `load_meta_targets` (qui crée un fichier par défaut s'il est absent).
- [x] Ajouter les messages d'erreurs robustes utilisant `rich.console`.
- [x] Écrire les tests unitaires couvrant les cas nominaux et d'erreurs.

## Dev Agent Record
- **Implementation Notes:** Implémentation des modèles `MetaThreat` et `MetaTargetsRequest` dans `models/meta.py` avec `ConfigDict(extra='forbid')` pour garantir un typage strict. Le parseur dans `rules/meta_parser.py` intercepte `yaml.YAMLError` et `pydantic.ValidationError`, et affiche des messages explicites via Rich avant d'exécuter un `typer.Exit(code=1)`. Le fichier par défaut est créé correctement s'il n'existe pas.
- **Tests Added:** Ajout de `test_meta_parser.py` avec 5 tests couvrant : parsing valide, création du fichier par défaut, gestion d'erreurs YAML (YAMLError), gestion d'erreurs de schéma Pydantic (ValidationError), et rejet de champs extra (forbid extra).

### File List
- `src/ygo_ultime_deck/models/meta.py` (NEW)
- `src/ygo_ultime_deck/rules/meta_parser.py` (NEW)
- `tests/test_rules/test_meta_parser.py` (NEW)

## Change Log
- Ajout de la gestion et du parsing du fichier de configuration `meta_targets.yaml`.

## Senior Developer Review (AI)

### Review Summary
**Review Outcome:** Changes Requested
**Date:** 2026-06-12
**Agent Pipeline:** Blind Hunter (Adversarial), Edge Case Hunter (Boundary), Acceptance Auditor (Spec Compliance)

### Action Items
**Severity Breakdown:** 3 High | 3 Medium | 1 Low

- [x] [AI-Review][High] Fix `TypeError` on unpacking `**data` if the YAML root is a list or scalar (e.g. `data = [{"name": "Ash"}]`). Automatically wrap it in `{"threats": data}` if it's a list.
- [x] [AI-Review][High] Catch `OSError` and `UnicodeDecodeError` during file read to prevent raw Python stack traces.
- [x] [AI-Review][High] Optimize default file creation: return the default `MetaTargetsRequest` from memory instead of hitting the disk twice (write then read).
- [x] [AI-Review][Medium] Enforce strict Pydantic rules on `MetaThreat`: strip whitespace on `name`, restrict `count` to `1 <= count <= 3`.
- [x] [AI-Review][Medium] Add missing test coverage for edge cases: `OSError`, `UnicodeDecodeError`, empty file (`data is None`), and non-dict YAML roots.
- [x] [AI-Review][Low] Remove unused imports (`MetaThreat` in `meta_parser.py`, `yaml` in `test_meta_parser.py`).

### Deferred Items
- [AI-Review][Defer] The parser uses `typer.Exit(1)`. Although flagged as an anti-pattern by the adversarial review, it strictly follows the existing pattern from `rules/config.py`. Refactoring this is deferred to a technical debt sprint.
- [AI-Review][Defer] The `category` field remains an unvalidated string instead of an Enum, allowing flexibility for users to define their own categories for now.

## Completion Status
- **Status Update:** done
- **Note:** Initial story definition completed.
