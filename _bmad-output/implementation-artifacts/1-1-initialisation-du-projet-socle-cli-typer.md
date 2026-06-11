---
baseline_commit: NO_VCS
---
# Story 1.1: Initialisation du Projet & Socle CLI (Typer)

**Status:** in-progress
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

- [ ] Task 1: Initialize project with uv
- [ ] Task 2: Configure pyproject.toml and dependencies
- [ ] Task 3: Create project structure and CLI entry point
- [ ] Task 4: Add simple pytest to verify CLI runs

## Dev Agent Record

### Debug Log
*(Notes will be added here during implementation)*

### Completion Notes
*(Final notes will be added here when complete)*

## File List
*(Changed files will be listed here)*

## Change Log
*(Changes will be recorded here)*

## Completion Status
- **Status Update:** ready-for-dev
- **Note:** Ultimate context engine analysis completed - comprehensive developer guide created.
