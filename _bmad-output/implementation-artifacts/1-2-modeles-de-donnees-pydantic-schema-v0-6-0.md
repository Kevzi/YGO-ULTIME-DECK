---
baseline_commit: 46f42b2
---
# Story 1.2: Modèles de Données Pydantic (Schéma v0.6.0)

**Status:** done
**Epic:** 1 - Initialisation et Synchronisation de la Base de Données YGO

## Story Requirements

**User Story:**
As a système de traitement,
I want disposer de modèles Pydantic stricts (`CardModel`) basés sur le schéma YGOJSON,
So that les données transitent dans le pipeline sous forme d'objets purs, garantissant le "Thread-Safety" pour le multiprocessing.

**Acceptance Criteria:**
- **Given** les spécifications du schéma YGOJSON v0.6.0
- **When** le système instancie une carte (y compris avec des champs manquants comme `series` ou un type "Mot-clé" réservé en Python)
- **Then** Pydantic valide les données via `Field(alias="type")`
- **And** l'objet généré est 100% sérialisable (Picklable) sans aucun état persistant.

## Developer Context & Guardrails

### Technical Requirements
- Créer le modèle principal `CardModel` dans `src/ygo_ultime_deck/models/card.py`.
- Utiliser `pydantic.BaseModel`.
- S'assurer que le champ JSON `type` est mappé à `card_type` en Python via `Field(alias="type")`.
- Permettre aux champs optionnels d'être nuls ou manquants en douceur sans faire crasher l'instanciation (ex: monstres sans effet, magies sans ATK).

### Architecture Compliance
- **Data Boundaries:** Les données doivent être de pures structures (Pydantic V2), aucun verrou ou session à l'intérieur. Ceci est vital pour le `ProcessPoolExecutor` (Multiprocessing).
- **Naming Patterns:**
  - Classes en `PascalCase` (ex: `CardModel`).
  - Attributs en `snake_case` même si le JSON d'origine est différent (utiliser `alias` ou la conversion native Pydantic).
- Conserver la pureté fonctionnelle absolue.

### Library/Framework Requirements
- **Pydantic V2**: Utiliser `ConfigDict` pour la configuration des modèles. Privilégier `model_dump()` au lieu de `dict()` et `model_validate()` au lieu de `parse_obj()`.

### File Structure Requirements
```text
ygo_ultime_deck/
├── src/
│   └── ygo_ultime_deck/
│       ├── models/
│       │   ├── __init__.py
│       │   └── card.py       # Validation stricte du schéma YGOJSON v0.6.0
```

### Testing Requirements
- Ajouter des tests dans `tests/test_models/test_card.py`.
- Vérifier la présence de `tests/test_models/__init__.py`.
- Tester l'instanciation avec `type` -> `card_type`.
- Tester la robustesse face aux champs manquants (champs optionnels).
- Vérifier que l'objet est bien "Picklable" (utiliser le module standard `pickle` dans le test).

## Previous Story Intelligence
- La base CLI et la gestion d'erreurs ont été sécurisées (Story 1.1 + Code Review). Les exceptions inattendues seront gérées correctement par `sys.excepthook`.

## Git Intelligence
- Le projet a récemment ajouté des correctifs pour s'assurer que les fichiers `__init__.py` de tests sont présents et que le typage `rich` est listé. Maintenir ces standards stricts.

## Tasks/Subtasks
- [x] Task 1: Créer le fichier `src/ygo_ultime_deck/models/card.py` et `__init__.py`.
- [x] Task 2: Définir `CardModel` avec les attributs nécessaires pour une carte Yu-Gi-Oh (id, name, type/card_type, desc, race, atk, def, level, attribute, etc.) en respectant les alias Pydantic.
- [x] Task 3: Créer les tests correspondants (incluant un test `pickle`) dans `tests/test_models/`.
- [x] Task 4: S'assurer du formatage via Ruff et exécution de pytest.

## Completion Status
- **Status Update:** done
- **Note:** Ultimate context engine analysis completed - comprehensive developer guide created

## Dev Agent Record
### Implementation Plan
- Implemented TDD approach (Red-Green-Refactor).
- Created `CardModel` mapping `type` to `card_type` and `def` to `def_`.
- Ensured fields are optional where required (e.g., `atk`, `race`).
- Ensured pickling works natively with Pydantic BaseModel.

### File List
- `src/ygo_ultime_deck/models/__init__.py`
- `src/ygo_ultime_deck/models/card.py`
- `tests/test_models/__init__.py`
- `tests/test_models/test_card.py`

### Change Log
- Added initial Pydantic models for YGOJSON schema v0.6.0.
- Implemented test suite including pickling and serialization tests.

### Completion Notes
- ✅ All acceptance criteria met. Tests passed, code linted via Ruff.

### Review Findings
- [x] [Review][Patch] Handling "?" for atk/def — YGOJSON frequently uses "?" for cards with variable stats. Create a validator.
- [x] [Review][Patch] Unconstrained string types — Fields like `attribute` and `race` are naked strings. Strictly type them with `Enum`.
- [x] [Review][Patch] String IDs — Numeric ID receives string with leading zeros. Change to `str`.
- [x] [Review][Patch] Use `model_validate()` [tests/test_models/test_card.py:17]
- [x] [Review][Patch] Missing exports in `__init__.py` [src/ygo_ultime_deck/models/__init__.py:1]
- [x] [Review][Patch] Hardcoded duplicated fixtures in tests [tests/test_models/test_card.py:6]
- [x] [Review][Patch] Weak assertions in `test_card_is_picklable` [tests/test_models/test_card.py:56]
- [x] [Review][Patch] Zero negative testing for validation errors [tests/test_models/test_card.py]
- [x] [Review][Patch] Untested complex types like `linkmarkers` [tests/test_models/test_card.py]
- [x] [Review][Patch] Clunky test assertions using `getattr` [tests/test_models/test_card.py:38]
- [x] [Review][Patch] Missing bounds validation (atk >= 0, level) [src/ygo_ultime_deck/models/card.py:19]
