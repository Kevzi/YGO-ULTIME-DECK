---
baseline_commit: 46f42b22ccca45bae82f54cbe7f2e967ffd20464
# Story 2.2: Fichier de Configuration Externe (tags_rules.yaml)

**Status:** ready-for-dev
**Epic:** 2 - Personnalisation et Auto-Tagging Sémantique

## Story Requirements

**User Story:**
As a concepteur de deck (utilisateur avancé),
I want définir le dictionnaire liant les mots-clés aux "Tags" dans un fichier `config/tags_rules.yaml`,
So that je puisse modifier l'intelligence du système ou ajouter de nouvelles règles sans jamais avoir à retoucher le code source Python.

**Acceptance Criteria:**
- **Given** un fichier `tags_rules.yaml` défini par l'utilisateur
- **When** le système initialise l'Epic 2
- **Then** l'application charge ce fichier de manière sécurisée (gestion de `FileNotFoundError` avec Typer)
- **And** injecte ces règles dynamiquement dans le Moteur Regex.

## Developer Context & Guardrails

### Technical Requirements
- Créer le dossier `config/` à la racine du projet s'il n'existe pas, et générer un fichier d'exemple `tags_rules.yaml` (ou le charger s'il existe).
- Développer une fonction de chargement (par exemple dans `src/ygo_ultime_deck/rules/config_loader.py` ou intégré dans `__init__.py` du module rules) qui lit le fichier YAML et retourne le dictionnaire `dict[str, str]` attendu par `RegexTagger`.
- Si le fichier `config/tags_rules.yaml` n'existe pas, le système doit lever une erreur proprement ou créer un fichier par défaut, selon l'approche de résilience choisie, mais le `FileNotFoundError` doit être géré avec `typer.Exit(1)` (s'il est intercepté par le main) ou géré gracieusement.
- Les règles YAML devront supporter la casse. L'utilisateur devra écrire `(?i)` dans ses règles s'il souhaite que la règle soit insensible à la casse (comportement décidé lors de la Story 2.1).

### Architecture Compliance
- **Data Boundaries:** Les fichiers YAML dans `config/` sont les frontières de configuration : le script Python ne contient AUCUNE règle métier en dur.
- **Error Handling Patterns:** L'absence ou la mauvaise configuration du fichier YAML doit déclencher un arrêt gracieux via `typer.Exit(code=1)` et l'utilisation de `Rich` pour afficher l'erreur, et non une stacktrace brute.

### Library/Framework Requirements
- `pyyaml` (déjà présent dans les dépendances `pyproject.toml`).
- `typer` et `rich` pour la gestion des erreurs.

### File Structure Requirements
- `config/tags_rules.yaml` (Fichier d'exemple / modèle)
- `src/ygo_ultime_deck/rules/config.py` (ou `loader.py`) pour la logique de lecture.
- `tests/test_rules/test_config.py` pour valider le chargement (et la gestion d'erreur).

### Testing Requirements
- Créer un fichier YAML temporaire (via les fixtures pytest, ex: `tmp_path`) pour valider la bonne conversion du YAML en `dict[str, str]`.
- Vérifier le comportement du chargeur lorsque le fichier n'existe pas (doit gérer `FileNotFoundError` ou lever une exception qui sera rattrapée par le CLI).
- Vérifier le comportement si le fichier YAML est mal formaté (YamlError).

## Previous Story Intelligence
- Dans la Story 2.1, nous avons supprimé le flag `re.IGNORECASE` codé en dur pour le moteur Regex. Il faut documenter dans les commentaires du `tags_rules.yaml` généré par défaut que les utilisateurs doivent utiliser `(?i)` s'ils souhaitent que leurs regex soient insensibles à la casse.
- Le `RegexTagger` est prêt à consommer directement le résultat de ce chargement YAML.

## Git Intelligence
- Maintenir le respect des normes `Ruff` (aucun import inutile).
- Les commits récents (Story 2.1) ont solidifié le typage avec des annotations modernes (`dict`, `re.Pattern`). Suivre cette tendance.

## Project Context Reference
- Le projet vise des performances massives, mais le chargement de cette configuration se fait à l'initialisation, donc l'I/O disque est acceptable à ce stade.

## Tasks / Subtasks
- [x] Créer le dossier `config/` et un fichier d'exemple `tags_rules.yaml`.
- [x] Créer `src/ygo_ultime_deck/rules/config.py` contenant une fonction pour charger ce fichier YAML.
- [x] Gérer l'erreur `FileNotFoundError` avec `typer.Exit(1)` si le fichier YAML n'est pas trouvé.
- [x] Créer les tests unitaires dans `tests/test_rules/test_config.py` pour valider le chargement et la gestion d'erreurs.
- [x] Vérifier que le linter Ruff et les tests pytest passent.

### Review Findings
- [x] [Review][Patch] Missing dynamic injection into Regex Engine [src/ygo_ultime_deck/rules/config.py]
- [x] [Review][Patch] Missing runtime creation of config/ directory and example file [src/ygo_ultime_deck/rules/config.py]
- [x] [Review][Patch] Error Output Routing (use stderr) [src/ygo_ultime_deck/rules/config.py]
- [x] [Review][Patch] Naive File Handling (PermissionError) [src/ygo_ultime_deck/rules/config.py]
- [x] [Review][Patch] Destructive Type Coercion (validate strings instead of casting) [src/ygo_ultime_deck/rules/config.py]
- [x] [Review][Patch] Mishandling Empty Configuration Files [src/ygo_ultime_deck/rules/config.py]
- [x] [Review][Patch] Platform-Dependent Encoding in the Test Suite [tests/test_rules/test_config.py]
- [x] [Review][Patch] Incomplete Test Coverage for edge cases [tests/test_rules/test_config.py]
- [x] [Review][Defer] Inconsistent Localization — deferred, pre-existing
- [x] [Review][Defer] Global State Side-Effects (Console) — deferred, pre-existing
- [x] [Review][Defer] Missing Formal Schema Validation (Pydantic) — deferred, pre-existing

## Completion Status
- **Status Update:** done
- **Note:** Implementation complete.

## Dev Agent Record
### Debug Log
- N/A

### Completion Notes
- Création du script `config.py` pour le chargement du YAML via `pyyaml`.
- Gestion des erreurs `FileNotFoundError` et `yaml.YAMLError` intégrée avec `Typer` et `Rich`.
- Création du fichier d'exemple `config/tags_rules.yaml` documentant l'utilisation du flag `(?i)`.
- Les tests unitaires (dont les validations de `Exit(1)`) passent avec succès à 100%.

## File List
- `config/tags_rules.yaml` (new)
- `src/ygo_ultime_deck/rules/config.py` (new)
- `tests/test_rules/test_config.py` (new)

## Change Log
- Ajout du module de configuration externe pour injecter dynamiquement les règles de tags Regex.
