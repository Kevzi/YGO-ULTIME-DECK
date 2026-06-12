---
# Story 1.3: Téléchargeur YGOJSON (Gestion du Cache)

**Status:** ready-for-dev
**Epic:** 1 - Initialisation et Synchronisation de la Base de Données YGO

## Story Requirements

**User Story:**
As a utilisateur CLI,
I want pouvoir utiliser une commande `ygo-deck --update`,
So that le système télécharge de manière asynchrone l'archive `aggregate.zip` depuis YGOJSON et la stocke dans le dossier local `/data/cache/`.

**Acceptance Criteria:**
- **Given** une connexion internet active
- **When** l'utilisateur exécute `ygo-deck --update`
- **Then** l'application affiche une barre de progression `Rich`
- **And** le fichier `aggregate.zip` est téléchargé et sauvegardé correctement dans le cache local
- **And** si le réseau coupe, une erreur élégante est affichée via `typer.Exit(1)` au lieu d'une stacktrace brute.

## Developer Context & Guardrails

### Technical Requirements
- Implémenter le téléchargement dans `src/ygo_ultime_deck/ingestion/downloader.py`.
- Intégrer un flag CLI `--update` ou une commande `update` dans `src/ygo_ultime_deck/main.py` via `Typer`.
- Le dossier de destination absolu ou relatif doit cibler `data/cache/` à la racine du projet. Ce répertoire doit être créé automatiquement s'il n'existe pas lors de l'exécution.
- Gérer l'asynchronisme du téléchargement (recommandation : bibliothèque `httpx` pour de l'I/O asynchrone avec `asyncio`).
- L'URL cible pour télécharger le schéma YGOJSON (archive contenant toutes les cartes) est généralement configurable, mais pointer par défaut vers l'archive YGOJSON standard (ex: `https://json.yugioh.com/api/v0.6.0/aggregate.zip` - vérifiez ou laissez en constante facilement modifiable).

### Architecture Compliance
- **Data Boundaries:** Le dossier `data/cache/` agit comme frontière réseau de l'application. L'architecture est pensée "Offline-First", donc l'application ne fait AUCUNE requête réseau en dehors du moment où l'utilisateur lance l'outil explicitement avec `--update`.
- **Process & Error Handling Patterns:** Le système métier lève des exceptions classiques (ex: erreurs réseau). La couche CLI (dans `main.py` ou au bord du downloader) intercepte TOUTES ces exceptions pour faire un `raise typer.Exit(code=1)` et utiliser `Rich` (ex: `console.print("[bold red]Erreur de connexion...[/bold red]")`) au lieu d'une stacktrace.

### Library/Framework Requirements
- `Typer` et `Rich` (déjà installés) : Utiliser `rich.progress` pour la barre de téléchargement.
- Ajouter `httpx` (ou équivalent asynchrone) via la commande `uv add httpx`.

### File Structure Requirements
```text
ygo_ultime_deck/
├── data/
│   └── cache/                   # Créé dynamiquement par le script si absent
├── src/
│   └── ygo_ultime_deck/
│       ├── main.py              # Ajout de l'argument CLI Typer
│       ├── ingestion/
│       │   ├── __init__.py
│       │   └── downloader.py    # Logique de téléchargement asynchrone
```

### Testing Requirements
- Créer les tests dans `tests/test_ingestion/test_downloader.py`.
- **Ne faire aucune requête réseau réelle dans les tests.** Utiliser le mock (via `pytest-httpx` par exemple, ajoutable via `uv add --dev pytest-httpx`).
- Tester spécifiquement :
  - Le cas passant (création du dossier, sauvegarde du fichier).
  - Le cas d'erreur réseau (Timeout, 404, etc.) et s'assurer que ça coupe proprement sans stacktrace non gérée.

## Previous Story Intelligence
- **Story 1.1 / 1.2 :** L'architecture du CLI avec Typer a été mise en place avec succès. L'utilisation du linter `Ruff` est obligatoire. Continuez d'utiliser les types stricts (Enum, BaseModel, types Python complets) sur chaque méthode.

## Git Intelligence
- Le linter Ruff impose des normes strictes de qualité (vu lors des corrections de la Story 1.2). Ne pas oublier les Docstrings pour les modules et les fonctions publiques, ni les fichiers `__init__.py` dans les dossiers de tests.

## Tasks/Subtasks
- [x] Task 1: Installer les dépendances HTTP (`httpx`) et de test (`pytest-httpx`) via `uv`.
- [x] Task 2: Développer `src/ygo_ultime_deck/ingestion/downloader.py` avec `httpx.AsyncClient` et `rich.progress`.
- [x] Task 3: Modifier `main.py` pour ajouter l'option `--update`.
- [x] Task 4: Gérer les erreurs réseau élégamment et quitter avec `typer.Exit(1)`.
- [x] Task 5: Rédiger les tests dans `tests/test_ingestion/test_downloader.py`.
- [x] Task 6: Exécuter `uv run pytest tests` et `uv run ruff check --fix src tests`.

## Dev Agent Record
### Implementation Plan
- Installed `httpx`, `pytest-httpx`, and `pytest-asyncio` using `uv`.
- Created `tests/test_ingestion/test_downloader.py` with mock HTTP responses for success and error cases using `httpx_mock`.
- Created `src/ygo_ultime_deck/ingestion/downloader.py` with asynchronous streaming via `httpx` and download tracking using `rich.progress`.
- Added the `--update` flag inside `src/ygo_ultime_deck/main.py`.
- Ensured graceful error handling using Typer Exit.

### File List
- `pyproject.toml`
- `src/ygo_ultime_deck/main.py`
- `src/ygo_ultime_deck/ingestion/__init__.py` (New)
- `src/ygo_ultime_deck/ingestion/downloader.py` (New)
- `tests/test_ingestion/__init__.py` (New)
- `tests/test_ingestion/test_downloader.py` (New)

### Change Log
- Added `httpx` logic for fetching YGOJSON aggregate zip efficiently with streaming and progress bar.
- Added `pytest-httpx` async test suite to prevent regressions.

## Completion Status
- **Status Update:** done
- **Note:** Ultimate context engine analysis completed - comprehensive developer guide created

### Review Findings
- [x] [Review][Patch] Blocking I/O inside Async Event Loop [src/ygo_ultime_deck/ingestion/downloader.py]
- [x] [Review][Patch] Leftover Corrupted Files on Failure [src/ygo_ultime_deck/ingestion/downloader.py]
- [x] [Review][Patch] Hardcoded, Unsafe Relative Path for Cache [src/ygo_ultime_deck/main.py]
- [x] [Review][Patch] Pointless Lazy Loading (httpx imported globally) [src/ygo_ultime_deck/main.py]
- [x] [Review][Patch] Missing Timeout Configuration [src/ygo_ultime_deck/ingestion/downloader.py]
- [x] [Review][Patch] Fragile Header Parsing (Content-Length) [src/ygo_ultime_deck/ingestion/downloader.py]
- [x] [Review][Patch] Brittle Test Mocks (Hardcoded URL) [tests/test_ingestion/test_downloader.py]
- [x] [Review][Patch] Missing test for CLI graceful exit on network error [tests/test_ingestion/test_downloader.py]
- [x] [Review][Patch] Missing test for 404 HTTP errors [tests/test_ingestion/test_downloader.py]
- [x] [Review][Patch] HTTP 4xx/5xx responses treated as unexpected errors [src/ygo_ultime_deck/main.py]
- [x] [Review][Patch] Missing docstrings for public functions and modules [tests/test_ingestion/test_downloader.py]
- [x] [Review][Defer] Hardcoded API Versioning [src/ygo_ultime_deck/ingestion/downloader.py] — deferred, pre-existing
