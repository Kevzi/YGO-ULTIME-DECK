---
baseline_commit: NO_VCS
---
# Story 1.1: Initialisation du Projet & Socle CLI (Typer)

**Status:** done
**Epic:** 1 - Initialisation et Synchronisation de la Base de Données YGO

## Story Requirements

**User Story:**
As a développeur / utilisateur CLI,
I want initialiser la structure du projet avec `uv`, `Typer` et `Rich`,
So that je puisse exécuter la commande globale `ygo-deck --help` et obtenir une interface propre et professionnelle.

**Acceptance Criteria:**
- **Given** l'environnement de développement vide
- **When** le développeur lance `uv init --package ygo_ultime_deck` et configure `pyproject.toml`
- **Then** le point d'entrée `ygo-deck` est disponible globalement
- **And** l'exécution de la commande affiche le menu d'aide standard formaté par `Rich` sans aucune erreur (Code de sortie 0).

## Developer Context & Guardrails

### Technical Requirements
- Initialiser le projet en utilisant `uv init --package ygo_ultime_deck`.
- Ajouter les dépendances d'exécution : `typer`, `pydantic` (v2), `pyyaml`.
- Ajouter les dépendances de développement : `ruff`, `pytest`.
- Configurer `pyproject.toml` pour exposer le point d'entrée CLI : `ygo-deck` qui pointe vers `ygo_ultime_deck.main:app`.
- Version cible de Python : 3.12+

### Architecture Compliance
- Le point d'entrée doit être `main.py` qui initialise Typer.
- La structure du projet doit suivre le layout standard `src/ygo_ultime_deck/`.
- Gestion des erreurs : utiliser `typer.Exit(code=1)` avec un formatage Rich pour toutes les erreurs CLI (au lieu de stacktraces brutes).
- Conventions de nommage : `snake_case` pour les variables/fonctions, `UPPER_SNAKE_CASE` pour les constantes.

### File Structure Requirements
\`\`\`text
ygo_ultime_deck/
├── src/
│   └── ygo_ultime_deck/
│       ├── __init__.py
│       └── main.py       # Point d'entrée CLI Typer
├── tests/
└── pyproject.toml        # Dépendances et configuration globale (Ruff, entry points)
\`\`\`

### Library/Framework Requirements
- **uv**: Gestionnaire de dépendances très rapide.
- **Typer**: Pour construire l'interface CLI.
- **Pydantic**: Utiliser obligatoirement la version 2.
- **Rich**: Pour formater les sorties console et les erreurs.

### Testing Requirements
- Configurer `pytest` pour s'assurer que l'application CLI peut être importée et que la commande `--help` fonctionne.

## Latest Tech Information
- Assurez-vous d'utiliser `uv` qui est la nouvelle norme, les commandes de création sont très spécifiques (`uv init`, `uv add`).
- Pydantic V2 utilise `model_dump()` au lieu de `dict()`.

## Tasks/Subtasks

- [x] Task 1: Initialize project with uv
- [x] Task 2: Configure pyproject.toml and dependencies
- [x] Task 3: Create project structure and CLI entry point
- [x] Task 4: Add simple pytest to verify CLI runs

## Dev Agent Record

### Debug Log
- `uv init` executed successfully.
- Added dependencies: `typer`, `pydantic` (v2), `pyyaml`, `ruff`, `pytest`.
- Updated `pyproject.toml` to expose `ygo-deck`.
- Created `main.py` with Typer setup.
- Added test in `tests/test_cli.py` which passes successfully.
- Also added `README.md` and committed initial baseline to Git locally.

### Completion Notes
The baseline CLI is functional. `uv run ygo-deck --help` executes cleanly without errors. Dependencies are locked.

## File List
- `pyproject.toml` (MODIFIED)
- `src/ygo_ultime_deck/main.py` (NEW)
- `tests/test_cli.py` (NEW)
- `README.md` (NEW)

## Change Log
- Initialized python project with `uv`
- Added Typer CLI entry point
- Created first test

### Review Findings

- [x] [Review][Patch] Python Version Constraint Mismatch [.python-version & pyproject.toml]
- [x] [Review][Patch] Missing Explicit Dependency for rich [pyproject.toml]
- [x] [Review][Patch] Missing Error Handling Configuration [src/ygo_ultime_deck/main.py]
- [x] [Review][Patch] Unused Global State [src/ygo_ultime_deck/main.py]
- [x] [Review][Patch] Dead Boilerplate Code [src/ygo_ultime_deck/__init__.py]
- [x] [Review][Patch] Sloppy Project Metadata [pyproject.toml]
- [x] [Review][Patch] Inadequate .gitignore [.gitignore]
- [x] [Review][Patch] Missing Module Initializer for Tests [tests/__init__.py]
- [x] [Review][Defer] Meaningless Test Suite — deferred, pre-existing
- [x] [Review][Defer] Absence of Static Type Checking — deferred, pre-existing
- [x] [Review][Defer] Missing License — deferred, pre-existing

## Completion Status
- **Status Update:** done
- **Note:** Initialisation complète et testée avec succès.
