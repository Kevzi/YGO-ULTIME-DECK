---
baseline_commit: 46f42b22ccca45bae82f54cbe7f2e967ffd20464
# Story 2.1: Moteur d'Expressions Régulières (Regex PSCT)

**Status:** done
**Epic:** 2 - Personnalisation et Auto-Tagging Sémantique

## Story Requirements

**User Story:**
As a moteur de catégorisation,
I want utiliser des expressions régulières (Regex) pré-compilées pour scanner les textes d'effets des cartes,
So that l'identification des mécaniques de jeu (ex: "Add 1 card", "Special Summon") soit quasi-instantanée et ne dépende pas d'une intelligence artificielle (NLP) lourde.

**Acceptance Criteria:**
- **Given** un objet `CardModel` contenant un texte d'effet de type PSCT
- **When** la fonction de tagging sémantique scanne la description
- **Then** l'algorithme fait correspondre le texte avec les Regex sans crash (même sur des textes très longs ou complexes)
- **And** attribue le tag adéquat dans un temps de calcul minimal.

## Developer Context & Guardrails

### Technical Requirements
- Créer ou mettre à jour le module de règles, spécifiquement `src/ygo_ultime_deck/rules/tagger.py`.
- Le moteur doit exposer une fonction recevant un objet `CardModel` et une série de règles Regex.
- Il doit appliquer les expressions régulières (idéalement pré-compilées via `re.compile()`) sur le texte de l'effet de la carte (`desc`).
- Le système de tagging doit enrichir l'objet avec ses tags. Pour respecter l'immuabilité et la pureté, le module devrait retourner un nouveau modèle Pydantic, par exemple `TaggedCardModel`, héritant de `CardModel` avec un attribut `tags: list[str]`.

### Architecture Compliance
- **Data Boundaries:** Ce module est la deuxième étape du pipeline unidirectionnel : `Ingestion -> Rules`. Il ne fait pas d'appels externes, il reçoit des `CardModel` purs.
- **Data Purity:** Pydantic doit toujours être utilisé. Les modèles instanciés par ce module devront être picklables pour l'étape suivante (Engine).
- **Performance:** Les Regex doivent être pré-compilées au chargement des règles pour éviter des pénalités lors de la boucle sur les milliers de cartes.

### Library/Framework Requirements
- `re` (Standard Python library).
- `pydantic` (déjà installé, pour le `TaggedCardModel`).

### File Structure Requirements
- `src/ygo_ultime_deck/models/card.py` (Mise à jour potentielle pour intégrer `TaggedCardModel` ou `tags` optionnel).
- `src/ygo_ultime_deck/rules/tagger.py` (Nouveau module pour la logique Regex).
- `tests/test_rules/test_tagger.py` (Tests unitaires associés).

### Testing Requirements
- Créer une suite de tests unitaires simulant différentes descriptions complexes PSCT (Problem-Solving Card Text).
- Vérifier que le moteur ne plante pas sur des textes inattendus ou très longs.
- Mesurer que l'affectation du tag se fait correctement selon une regex définie (ex: `r"Add .* from your Deck to your hand"` pour le tag "Searcher").

## Previous Story Intelligence
- Le `CardModel` actuel est configuré avec `extra="ignore"`. Les attributs non explicitement définis sont ignorés. Il est préférable de créer un sous-modèle Pydantic ou de modifier `CardModel` pour y ajouter `tags: list[str] = Field(default_factory=list)`.
- Lors de l'Epic 1 (Ingestion), le parser a été rendu ultra-résilient avec des try/except et des vérifications de types pour ignorer les cartes inattendues. Ce tagger devrait également gérer l'absence d'effets (ex: monstres normaux) sans lever d'exceptions.

## Git Intelligence
- Le projet respecte rigoureusement `Ruff` pour le formatage et le linting.
- Garder les docstrings selon les conventions établies et exécuter `uv run ruff check --fix` avant commit.

## Tasks / Subtasks
- [x] Mettre à jour `CardModel` ou créer `TaggedCardModel` avec un champ `tags`.
- [x] Créer `src/ygo_ultime_deck/rules/tagger.py` pour le moteur de scan Regex.
- [x] Pré-compiler un jeu de Regex d'exemple et l'appliquer sur la propriété `desc`.
- [x] Créer `tests/test_rules/test_tagger.py` pour valider la vitesse et la précision du Moteur Regex.
- [x] Valider avec `pytest` et corriger les erreurs de linting avec `ruff`.

### Review Findings
- [x] [Review][Defer] ReDoS / Backtracking Mitigation — deferred: Architecture Offline-First, règles internes sécurisées.
- [x] [Review][Patch] Regex Flags Inflexibles — `re.IGNORECASE` est codé en dur, empêchant les règles sensibles à la casse. Retiré.
- [x] [Review][Patch] Faux Positifs sur Monstres Normaux — Ignorer structurellement les monstres normaux.
- [x] [Review][Patch] Missing compilation safety [src/ygo_ultime_deck/rules/tagger.py:20]
- [x] [Review][Patch] Fragile Stats Validator [src/ygo_ultime_deck/models/card.py:180]
- [x] [Review][Patch] Tags key collision on instantiation [src/ygo_ultime_deck/rules/tagger.py:39]
- [x] [Review][Patch] Missing re.DOTALL for multi-line texts [src/ygo_ultime_deck/rules/tagger.py:20]
- [x] [Review][Patch] Pydantic performance bottleneck (use model_construct) [src/ygo_ultime_deck/rules/tagger.py:39]
- [x] [Review][Patch] Antiquated Type Hinting [src/ygo_ultime_deck/rules/tagger.py:2]
- [x] [Review][Patch] Redundant Defensive Checks on desc [src/ygo_ultime_deck/rules/tagger.py:33]
- [x] [Review][Patch] Missing test coverage for complex PSCT [tests/test_rules/test_tagger.py]
- [x] [Review][Patch] Missing programmatic speed validation [tests/test_rules/test_tagger.py]
- [x] [Review][Patch] Superficial Edge-Case Testing (fields preservation) [tests/test_rules/test_tagger.py]
- [x] [Review][Defer] Data Destruction (extra="ignore") [src/ygo_ultime_deck/models/card.py:155] — deferred, pre-existing

## Project Context Reference
Ce module (Rules/Tagger) sera nourri par le YAML lors de la prochaine story, mais il doit d'abord disposer du cœur de la mécanique Regex (Story 2.1) avant de dynamiser ses inputs (Story 2.2).

## Completion Status
- **Status Update:** done
- **Note:** Ultimate context engine analysis completed - comprehensive developer guide created

## Dev Agent Record
### Debug Log
- N/A

### Completion Notes
- Implémentation du modèle `TaggedCardModel` héritant de `CardModel`.
- Développement de `RegexTagger` pour analyser les textes avec résilience et `re.IGNORECASE`.
- Ajout de la suite de tests complètes simulant différents comportements (basic, no match, multiple matches, very long string).
- Les vérifications Ruff et Pytest (y compris rétrocompatibilité) passent à 100%.

## File List
- `src/ygo_ultime_deck/models/card.py`
- `src/ygo_ultime_deck/rules/__init__.py`
- `src/ygo_ultime_deck/rules/tagger.py`
- `tests/test_rules/test_tagger.py`

## Change Log
- Ajout du tagger regex et du support Pydantic pour l'export des tags.
---
