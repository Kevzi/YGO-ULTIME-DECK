---
# Story 1.4: Parseur Résilient & Pré-filtrage Mémoire

**Status:** done
**Epic:** 1 - Initialisation et Synchronisation de la Base de Données YGO

## Story Requirements

**User Story:**
As a moteur d'ingestion,
I want décompresser le cache local et parser les cartes tout en ignorant les cartes illégales (Rush Duel, Banlist),
So that la RAM ne soit chargée qu'avec les cartes compétitives pertinentes, évitant les crashs sur des champs manquants (ex: Monstres Normaux).

**Acceptance Criteria:**
- **Given** le cache local `aggregate.zip` téléchargé
- **When** l'application initialise le pipeline de données
- **Then** elle extrait le JSON, ignore les cartes n'ayant pas le format "TCG" ou "OCG"
- **And** elle transforme chaque carte valide en `CardModel`
- **And** la fonction retourne la liste des modèles sans crasher, même face aux monstres normaux (qui n'ont pas de texte d'effet complexe).

## Developer Context & Guardrails

### Technical Requirements
- Le parser doit être implémenté dans `src/ygo_ultime_deck/ingestion/parser.py`.
- L'archive YGOJSON `aggregate.zip` doit être lue sans extraction physique sur le disque (utiliser le module natif `zipfile` pour lire le contenu en mémoire).
- Filtrage : Le JSON de l'archive YGOJSON liste les cartes. Il faut conserver uniquement celles jouables dans les formats TCG ou OCG standards (généralement via la clé `formats` ou `legalities`).
- Conversion : Chaque entité JSON conservée doit être instanciée via `ygo_ultime_deck.models.card.CardModel`.
- Tolérance aux pannes : Gérer les KeyError ou ValidationError de manière robuste via try/except. L'échec d'une carte ne doit pas bloquer le parsing des autres cartes.

### Architecture Compliance
- **Data Boundaries:** Les données du cache (`data/cache/aggregate.zip`) sont la seule source d'entrée. Aucun appel réseau.
- **Data Purity:** Le flux de données est unidirectionnel. La fonction retourne une liste de `CardModel` purs (Picklable), garantie par Pydantic, préparant la phase suivante (Moteur Regex).
- **Performance / Memory Safety:** Le pré-filtrage doit éliminer un maximum d'objets inutiles *avant* de charger tout l'environnement (Rush Duel, Skill Cards).

### Library/Framework Requirements
- `zipfile` et `json` (librairies standards Python).
- `pydantic` (déjà utilisé pour `CardModel`).

### File Structure Requirements
```text
ygo_ultime_deck/
├── src/
│   └── ygo_ultime_deck/
│       ├── ingestion/
│       │   ├── downloader.py    
│       │   └── parser.py        # Logique de décompression et filtrage
├── tests/
│   └── test_ingestion/
│       ├── test_downloader.py
│       └── test_parser.py       # Tests de la résilience du parser
```

### Testing Requirements
- Créer `tests/test_ingestion/test_parser.py`.
- Simuler un fichier zip en mémoire (ou un petit zip de test) contenant un sous-ensemble du schéma YGOJSON (une carte TCG valide, une carte Rush Duel, une carte avec données manquantes).
- Tester que le pré-filtrage conserve bien uniquement le TCG/OCG.
- S'assurer que le parser retourne bien une liste de `CardModel` et qu'aucune exception non gérée n'est levée pour une structure malformée isolée.

## Previous Story Intelligence
- **Story 1.2 & 1.3 :** Pydantic `CardModel` a été configuré avec `extra="ignore"` et des alias comme `Field(alias="type")`. Le module `downloader.py` enregistre le cache sous `data/cache/aggregate.zip`. Le parser devra pointer vers ce même chemin relatif sécurisé.

## Git Intelligence
- Pensez à utiliser `Ruff` (`uv run ruff check --fix`) et à bien annoter les docstrings. Utiliser des types stricts.

## Tasks / Subtasks
- [x] Task 1: Créer le module `src/ygo_ultime_deck/ingestion/parser.py`.
- [x] Task 2: Développer la fonction `load_and_parse_ygojson()` lisant depuis le `zipfile`.
- [x] Task 3: Implémenter la logique de filtrage (exclusion Rush Duel/Anime).
- [x] Task 4: Mapper les objets filtrés avec Pydantic (`CardModel`).
- [x] Task 5: Ajouter les tests (valide, format invalide, champs manquants) dans `test_parser.py`.
- [x] Task 6: Lancer `pytest` et `ruff` pour validation.

## Dev Agent Record
### Completion Status
- **Status Update:** done
- **Note:** Implementation of the resilient parser successfully completed with tests. Memory filtering ensures only valid TCG/OCG non-token cards are transformed into Pydantic models.

### Change Log
- Created `src/ygo_ultime_deck/ingestion/parser.py`
- Created `tests/test_ingestion/test_parser.py`

### File List
- `src/ygo_ultime_deck/ingestion/parser.py`
- `tests/test_ingestion/test_parser.py`

### Review Findings
- [x] [Review][Patch] Missing Banlist filtering — The parser only filters by TCG/OCG formats but does not check for banned cards as requested.
- [x] [Review][Patch] Incomplete resilience against malformed non-dictionary items [`src/ygo_ultime_deck/ingestion/parser.py:42`]
- [x] [Review][Patch] Original exception masked during cleanup [`src/ygo_ultime_deck/ingestion/downloader.py:34`]
- [x] [Review][Patch] Incomplete cleanup on failure or cancellation [`src/ygo_ultime_deck/ingestion/downloader.py:32`]
- [x] [Review][Patch] Unhandled BadZipFile exception [`src/ygo_ultime_deck/ingestion/parser.py:26`]
- [x] [Review][Patch] Unhandled JSONDecodeError exception [`src/ygo_ultime_deck/ingestion/parser.py:35`]
- [x] [Review][Patch] Iterating over dict keys if 'data' is missing [`src/ygo_ultime_deck/ingestion/parser.py:38`]
- [x] [Review][Patch] Missing Cleanup Assertion in Tests [`tests/test_ingestion/test_downloader.py`]
- [x] [Review][Defer] Memory Bloat in Parser — deferred, pre-existing
- [x] [Review][Defer] Inadequate Field Validation — deferred, pre-existing
- [x] [Review][Defer] Naive Stat Handling — deferred, pre-existing
- [x] [Review][Defer] Hardcoded API Version — deferred, pre-existing
- [x] [Review][Defer] Swallowed Exceptions in CLI — deferred, pre-existing
---
