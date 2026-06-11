---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
inputDocuments: []
workflowType: 'architecture'
project_name: 'YGO ULTIME DECK'
user_name: 'Kevin'
date: '2026-06-09'
lastStep: 8
status: 'complete'
completedAt: '2026-06-09'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Architecture Validation Results

### Coherence Validation ✅

**Decision Compatibility:**
Le choix de `uv` + `Typer` + `Pydantic` + `asyncio/ProcessPoolExecutor` forme une pile technologique (Stack) extrêmement cohérente. Pydantic garantit la pureté des données (Picklable) nécessaire au `ProcessPoolExecutor`, et l'orchestration `asyncio` prépare nativement le terrain pour FastAPI en V2 sans conflit de boucle d'événements.

**Pattern Consistency:**
Les patterns d'implémentation (flux unidirectionnel sans état partagé) soutiennent parfaitement le choix de l'architecture multiprocessing, évitant les verrous mortels (deadlocks).

**Structure Alignment:**
La séparation stricte entre `models/` (données), `engine/` (calcul asynchrone) et `config/` (règles métier) isole parfaitement les responsabilités.

### Requirements Coverage Validation ✅

**Epic/Feature Coverage:**
Les 4 fonctionnalités (Ingestion, Règles, Moteur Mathématique, Intelligence) possèdent toutes leur propre module dans `src/ygo_ultime_deck/` et leurs tests dans `tests/`.

**Functional Requirements Coverage:**
Le cache local, le parsing Regex, la simulation Monte-Carlo et l'export `.ydk` sont intégralement mappés à des fichiers spécifiques.

**Non-Functional Requirements Coverage:**
Le SLA de performance est couvert par le multiprocessing. La protection de la mémoire est garantie par `math_utils.py` (log-gamma) et le pré-filtrage strict de l'ingestion Pydantic.

### Implementation Readiness Validation ✅

**Decision Completeness:**
Toutes les décisions critiques sont prises et documentées avec les versions cibles (Python 3.12+, Pydantic V2).

**Structure Completeness:**
L'arborescence est exhaustive, incluant la configuration `pyproject.toml` avec son entry point CLI explicite `ygo-deck`.

**Pattern Completeness:**
Les conventions de nommage, de typage, de communication inter-processus et de gestion d'erreur avec `Typer`/`Rich` sont définies sans aucune ambiguïté.

### Gap Analysis Results

*Aucun manque critique identifié.* Les fondations sont complètes et prêtes pour l'ingénierie.

### Validation Issues Addressed

Toutes les ambiguïtés potentielles (comme la déclaration explicite du point d'entrée CLI) ont été traitées proactivement.

### Architecture Completeness Checklist

**Requirements Analysis**
- [x] Project context thoroughly analyzed
- [x] Scale and complexity assessed
- [x] Technical constraints identified
- [x] Cross-cutting concerns mapped

**Architectural Decisions**
- [x] Critical decisions documented with versions
- [x] Technology stack fully specified
- [x] Integration patterns defined
- [x] Performance considerations addressed

**Implementation Patterns**
- [x] Naming conventions established
- [x] Structure patterns defined
- [x] Communication patterns specified
- [x] Process patterns documented

**Project Structure**
- [x] Complete directory structure defined
- [x] Component boundaries established
- [x] Integration points mapped
- [x] Requirements to structure mapping complete

### Architecture Readiness Assessment

**Overall Status:** READY FOR IMPLEMENTATION

**Confidence Level:** High

**Key Strengths:**
- Séparation stricte et élégante des responsabilités logicielles.
- Architecture très robuste, taillée sur mesure pour une charge CPU massive.
- Transition vers l'interface Web (V2) garantie et anticipée sans dette technique.

**Areas for Future Enhancement:**
- Automatisation des mises à jour des fichiers `meta_targets.yaml` via un scraping web en V2.

### Implementation Handoff

**AI Agent Guidelines:**
- Follow all architectural decisions exactly as documented.
- Use implementation patterns consistently across all components.
- Respect project structure and boundaries.
- Refer to this document for all architectural questions.

**First Implementation Priority:**
Créer le script d'initialisation via `uv init --package ygo_ultime_deck`, ajouter les dépendances (`typer`, `pydantic`), et configurer le point d'entrée dans `pyproject.toml`.

## Project Structure & Boundaries

### Complete Project Directory Structure

```text
ygo_ultime_deck/
├── config/                      # Configuration utilisateur (Externalisée)
│   ├── tags_rules.yaml          # Règles Regex (F2)
│   ├── target_combos.yaml       # Combos à calculer (F3)
│   └── meta_targets.yaml        # Cibles du Counter-Matching (F4)
├── data/                        # Données locales (Ignoré par git)
│   └── cache/                   # Cache pour YGOJSON (aggregate.zip)
├── src/
│   └── ygo_ultime_deck/
│       ├── __init__.py
│       ├── main.py              # Point d'entrée CLI (Typer) + Boucle asyncio
│       ├── models/              # Modèles Pydantic partagés (Data Flow)
│       │   ├── __init__.py
│       │   ├── card.py          # Validation stricte du schéma YGOJSON v0.6.0
│       │   ├── deck.py          # Format de deck et sérialisation YDK
│       │   └── simulation.py    # Modèle de résultat pour le Math Engine
│       ├── ingestion/           # F1: YGOJSON Data Ingestion
│       │   ├── __init__.py
│       │   ├── downloader.py    # Gestion du '--update'
│       │   └── parser.py        # Lecture du cache et instanciation Pydantic
│       ├── rules/               # F2: Functional Categorization
│       │   ├── __init__.py
│       │   └── tagger.py        # Moteur d'expressions régulières (Regex)
│       ├── engine/              # F3: Mathematical Engine (Force Brute)
│       │   ├── __init__.py
│       │   ├── math_utils.py    # Algorithme log-gamma pour hypergeometric
│       │   ├── monte_carlo.py   # Orchestration des 100k itérations
│       │   └── worker.py        # Tâche unitaire pour le ProcessPoolExecutor
│       └── intelligence/        # F4: Counter-Matching Intelligence
│           ├── __init__.py
│           ├── matcher.py       # Algorithme d'immunité et évaluation
│           └── ydk_parser.py    # Import/Export des decks cibles (.ydk)
├── tests/                       # Couverture Pytest (Indépendante)
│   ├── test_ingestion/
│   ├── test_rules/
│   ├── test_engine/
│   └── test_intelligence/
├── pyproject.toml               # Dépendances uv et config Ruff (inclut l'entry point [project.scripts] ygo-deck = "ygo_ultime_deck.main:app")
└── README.md
```

### Architectural Boundaries

**API/CLI Boundaries:**
- Le fichier `main.py` est l'unique point d'entrée. Il interagit avec l'utilisateur via Typer/Rich, parse les arguments, initialise la boucle `asyncio` et lance le Pipeline.
- Les fichiers YAML dans `config/` sont les frontières de configuration : le script Python ne contient AUCUNE règle métier en dur.

**Component Boundaries:**
- Le dossier `models/` est le "contrat" central. Aucun autre module ne communique avec des dictionnaires natifs. L'Ingestion passe des `CardModel` aux `Rules`, qui passent des `TaggedCardModel` à l'`Engine`.

**Data Boundaries:**
- Le dossier `data/cache/` agit comme frontière réseau. Le script ne fait des requêtes HTTP externes (vers le site YGOJSON) que lorsque `downloader.py` est explicitement appelé. Autrement, le système est "Offline-First".

### Requirements to Structure Mapping

**Feature/Epic Mapping:**
- **F1 (Data Ingestion)** : Implémenté dans `src/ygo_ultime_deck/ingestion/` et `data/cache/`.
- **F2 (Categorization)** : Implémenté dans `src/ygo_ultime_deck/rules/` et configuré via `config/tags_rules.yaml`.
- **F3 (Math Engine)** : Implémenté dans `src/ygo_ultime_deck/engine/` avec délégation stricte au `worker.py` pour le multiprocessing.
- **F4 (Counter-Matching)** : Implémenté dans `src/ygo_ultime_deck/intelligence/`.

### Integration Points

**Internal Communication:**
- Le flux de données est unidirectionnel et orchestré par `main.py` : `Ingestion -> Rules -> Engine -> Intelligence -> YDK_Export`.

**Data Flow (Multiprocessing):**
- Le module `engine/monte_carlo.py` envoie des listes de paquets pré-filtrés (Pydantic models picklés) au `ProcessPoolExecutor`, qui exécute `worker.py` sur plusieurs cœurs. Le worker retourne des objets de type `SimulationResult` asynchrones.

## Implementation Patterns & Consistency Rules

### Pattern Categories Defined

**Critical Conflict Points Identified:**
5 zones où les agents IA pourraient faire des choix différents (Nommage Python/Pydantic, Options CLI, Sérialisation Multiprocessing, Gestion des erreurs).

### Naming Patterns

**Code Naming Conventions:**
- **Variables & Fonctions Python** : Strictement `snake_case` (ex: `calculate_hypergeometric()`).
- **Modèles Pydantic (Classes)** : Strictement `PascalCase` (ex: `CardModel`, `DecklistResult`).
- **Constantes** : Strictement `UPPER_SNAKE_CASE` (ex: `MAX_ITERATIONS`).

**API/Data Naming Conventions:**
- Les attributs Python doivent utiliser le `snake_case` même si le JSON d'origine (YGOJSON) utilise une autre casse. L'agent **DOIT** utiliser `Field(alias="originalName")` dans Pydantic pour faire le pont et nettoyer la donnée. Le mot-clé `type` (réservé en Python) doit toujours être mappé vers `card_type`.

### Structure Patterns

**Project Organization:**
- **Modèles de Données** : Tous les modèles Pydantic doivent être centralisés ensemble (ex: `src/ygo_ultime_deck/models/`).
- **Fichiers de Configuration** : Les fichiers YAML de l'utilisateur (`target_combos.yaml`, `meta_targets.yaml`) doivent résider dans un dossier `./config/` explicite.

### Format Patterns

**CLI Formats:**
- **Options Typer** : Les arguments en ligne de commande doivent toujours utiliser le `kebab-case` (ex: `--update-data`). Typer le fait nativement à partir du nom des fonctions, les agents ne doivent pas créer d'overrides (alias) contredisant cette norme.

### Communication Patterns

**Multiprocessing & State (Le plus critique):**
- **Règle d'or de Sérialisation** : TOUTES les données passées aux fonctions exécutées via `ProcessPoolExecutor` DOIVENT être des modèles Pydantic purs ou des types Python natifs. Il est **strictement interdit** de passer des instances de classes contenant des états non sérialisables (Pickle) tels que des verrous `asyncio.Lock`, des sessions HTTP ouvertes, ou des descripteurs de fichiers.

### Process Patterns

**Error Handling Patterns:**
- Le code du moteur métier lève des exceptions Python standards (ex: `ValueError`, `FileNotFoundError`).
- La couche CLI (le point d'entrée Typer) intercepte TOUTES ces exceptions et utilise `typer.Exit(code=1)` en affichant un message formaté via la librairie `Rich` au lieu de crasher avec une "Stacktrace" brute (sauf mode `--debug`).

### Enforcement Guidelines

**All AI Agents MUST:**
- Utiliser Pydantic pour TOUTE validation de données, sans exception.
- Éviter absolument toute variable globale mutée dans le module `math_engine.py` (Functional Purity).
- Formater le code généré pour satisfaire le linter `Ruff`.

### Pattern Examples

**Good Examples:**
```python
# Bon Pattern (Pydantic avec alias et évitement de mot-clé réservé)
class CardModel(BaseModel):
    card_type: str = Field(alias="type")
    
# Bon Pattern (CLI Exit élégant)
except ValueError as e:
    console.print(f"[bold red]Erreur critique : {e}[/bold red]")
    raise typer.Exit(1)
```

**Anti-Patterns:**
```python
# Mauvais Pattern (Casse incorrecte, utilisation de 'type' qui va écraser la fonction native Python)
class card_model(BaseModel):
    type: str 

# Mauvais Pattern (Print direct avec sys.exit)
except ValueError as e:
    print(e)
    sys.exit(1)
```

## Core Architectural Decisions

### Decision Priority Analysis

**Critical Decisions (Block Implementation):**
- Data Flow Architecture (Pydantic-driven Functional Pipeline)
- Multiprocessing Architecture (`asyncio` + `ProcessPoolExecutor`)

**Important Decisions (Shape Architecture):**
- API-Ready Orchestration (Préparation de la transition V2 via asynchronisme)

**Deferred Decisions (Post-MVP):**
- V2 Web Interface (FastAPI et stack Frontend reportés à la Phase 2)

### Data Architecture

**Pipeline Fonctionnel Unidirectionnel (Pydantic-Driven)**
- **Decision:** Le flux de données sera strictement unidirectionnel, sans état partagé global. L'orchestrateur passera les données d'un module à l'autre.
- **Version:** Pydantic V2
- **Rationale:** Permet une sérialisation (pickling) sûre, prérequis absolu pour passer de gros volumes de données entre les processus CPU. Garantit la validation stricte des énumérations du schéma YGOJSON (v0.6.0). Rend le code "Thread-Safe" et testable unitairement via `pytest`.

### Infrastructure & Performance

**Multiprocessing Hybride Asynchrone**
- **Decision:** Utilisation de la boucle `asyncio` pour l'orchestration I/O combinée à `ProcessPoolExecutor`.
- **Version:** Python 3.12+ (Standard Library)
- **Rationale:** Délègue les 100 000 itérations de Monte-Carlo sur plusieurs cœurs de processeur via `loop.run_in_executor()` sans bloquer le script. L'utilisation native de l'asynchronisme en V1 rendra le portage vers FastAPI (qui utilise la même boucle d'événements) quasiment instantané pour la V2 Web.

### Decision Impact Analysis

**Implementation Sequence:**
1. Setup du projet avec `uv` et `Typer`.
2. Implémentation du pipeline fonctionnel (Ingestion YGOJSON asynchrone -> Modèles Pydantic).
3. Développement du Math Engine isolé et scalable avec `ProcessPoolExecutor`.
4. Raccordement de l'Intelligence de Counter-Matching.

**Cross-Component Dependencies:**
- L'orchestrateur principal CLI devra gérer explicitement la boucle d'événements `asyncio`.
- Les modèles Pydantic générés par la couche d'Ingestion devront être dépourvus de toute méthode non-sérialisable pour survivre au transfert inter-processus.

## Starter Template Evaluation

### Primary Technology Domain

**Backend Python / CLI** basé sur l'analyse des exigences du projet.

### Starter Options Considered

1. **L'approche moderne `uv` + Typer (Recommandée)** : Initialisation native d'une structure de paquet propre via l'outil `uv` (standard de l'industrie), en combinant `Typer` pour les commandes et `Ruff` pour le linting. Offre un contrôle absolu sans code mort.
2. **typer-cli-template (L'approche "Boilerplate")** : Un dépôt communautaire tout-en-un incluant Poetry, Typer, Rich et des GitHub Actions préconfigurées. Rejeté car trop lourd et moins flexible pour notre algorithme spécifique.

### Selected Starter: Modern `uv` + Typer + Ruff

**Rationale for Selection:**
Puisque le projet est un algorithme mathématique extrêmement exigeant en performances (Monte-Carlo), nous avons besoin d'une base logicielle légère et maîtrisée de bout en bout. `uv` garantit une résolution instantanée des environnements virtuels Python. `Typer` (qui s'appuie sur Pydantic) permet de créer une architecture CLI très robuste, typée (valide parfaitement le schéma YGOJSON) et facile à relier plus tard à une API Web (FastAPI).

**Initialization Command:**

```bash
uv init --package ygo_ultime_deck
cd ygo_ultime_deck
uv add typer pydantic pyyaml
uv add --dev ruff pytest
```

**Architectural Decisions Provided by Starter:**

**Language & Runtime:**
- Python 3.12+ (fortement recommandé pour les bénéfices de performance).
- Typage strict imposé (via Pydantic et les annotations Python).

**Styling Solution:**
- Interface utilisateur en Ligne de Commande (CLI). `Typer` utilise nativement `Rich` sous le capot pour un affichage texte coloré et élégant.

**Build Tooling:**
- Gestionnaire de paquets et d'environnement : `uv` (via `pyproject.toml`).

**Testing Framework:**
- `pytest` pour des tests unitaires rapides et précis de l'algorithme hypergéométrique.

**Code Organization:**
Le standard de la communauté (layout `src/`) pour éviter les erreurs d'importation :
```text
ygo_ultime_deck/
├── src/
│   └── ygo_ultime_deck/
│       ├── __init__.py
│       └── main.py       # Point d'entrée CLI Typer
├── tests/
└── pyproject.toml        # Dépendances et configuration globale (Ruff, etc.)
```

**Development Experience:**
- Linter et Formateur ultra-rapide : `Ruff` (remplace avantageusement Flake8, Isort et Black).

**Note:** Project initialization using this command should be the first implementation story.

## Project Context Analysis

### Requirements Overview

**Functional Requirements:**
Le système est un moteur d'optimisation de deck en ligne de commande (Python) comprenant l'ingestion de données JSON massives avec mise en cache, un moteur de tagging dynamique basé sur des règles Regex externes, un calculateur probabiliste via Monte-Carlo, et une intelligence de "Counter-Matching" s'interfaçant nativement avec le format `.ydk`.

**Non-Functional Requirements:**
- Tolérance aux calculs longs : Le SLA autorise 15-30s pour garantir une précision absolue.
- Protection Mémoire : Implémentation stricte d'un algorithme logarithmique (ex: `math.lgamma`) pour éviter les crashs sur les grands calculs factoriels.
- API-Ready : L'utilisation de fichiers de configuration utilisateur (`tags_rules.yaml`, `target_combos.yaml`, `meta_targets.yaml`) prépare le système à être encapsulé derrière une API pour la future V2 Web.

**Scale & Complexity:**
Le système effectue potentiellement des centaines de milliers de boucles de simulation par requête, ce qui exige des décisions logicielles optimisées.
- Primary domain: Backend Python (CLI)
- Complexity level: Élevée (Complexité Algorithmique)
- Estimated architectural components: 5 (Data Cache/Ingestion, Rule Parser, Math Engine, Intelligence Engine, YDK Parser)

### Technical Constraints & Dependencies

- Dépendance stricte au schéma open-source YGOJSON v0.6.0.
- La structure doit pouvoir accueillir une éventuelle parallélisation (multithreading/multiprocessing) pour le moteur de Monte-Carlo si nécessaire.

### Cross-Cutting Concerns Identified

- Séparation stricte entre les "Règles métier" (fichiers YAML modifiables par l'utilisateur) et le "Moteur d'exécution" (script Python).
- Gestion efficace de l'empreinte RAM via un pré-filtrage strict des formats de cartes lors de l'ingestion.

