---
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
- [ ] Créer les modèles Pydantic pour les menaces (`MetaThreat`).
- [ ] Écrire la fonction de parsing `load_meta_targets` (qui crée un fichier par défaut s'il est absent).
- [ ] Ajouter les messages d'erreurs robustes utilisant `rich.console`.
- [ ] Écrire les tests unitaires couvrant les cas nominaux et d'erreurs.

## Dev Agent Record
- **Implementation Notes:** (To be filled by the dev agent)
- **Tests Added:** (To be filled by the dev agent)

### File List
- (To be filled by the dev agent)

## Change Log
- (To be filled by the dev agent)

## Completion Status
- **Status Update:** ready-for-dev
- **Note:** Initial story definition completed.
