---
baseline_commit: 3e606c89299f27af0f625042ef16fb14b55cc932
# Story 5.2: Intégration de la résolution dans l'Audit CLI

**Status:** ready-for-dev
**Epic:** 5 - Base de Données Cartes et Résolution d'IDs

## Story Requirements

**User Story:**
As a joueur Yu-Gi-Oh!,
I want que le module d'audit CLI utilise le `CardResolver` pour injecter les vrais IDs des cartes dans le fichier `.ydk`,
So that je puisse importer le résultat directement dans mon simulateur sans avoir des "11111111" partout.

**Acceptance Criteria:**
- **Given** une exécution réussie de la commande `ygo-deck audit` avec un noyau de deck (core) spécifié ou simulé
- **When** l'étape d'exportation YDK est atteinte
- **Then** le système initialise le `CardResolver` et résout les noms des cartes du deck simulé
- **And** le fichier `.ydk` exporté contient les vrais IDs des cartes correspondantes (par exemple `14558127` pour "Ash Blossom") au lieu d'une liste remplie de mock IDs génériques.
- **And** les cartes non trouvées utiliseront le mock ID de fallback sans faire crasher l'export.

## Developer Context & Guardrails

### Technical Requirements
- Le fichier `main.py` contient actuellement un decklist mocké avec des IDs fixes `[14558127] * opt_size`.
- Il faut extraire la liste réelle des noms de cartes du deck. Pour le MVP, si on n'a que "Starter", "Extender", "Garnet" et "Brick", le resolver ne les trouvera pas (et retournera le mock ID, ce qui est normal).
- Cependant, l'utilisateur a configuré ses "Starters" et "Garnets" dans `target_combos.yaml`. Il faut idéalement pouvoir extraire de VRAIS noms de cartes depuis ce fichier, ou utiliser l'argument CLI `--core` (ex: "Snake-Eye Ash") si fourni.
- Pour rester simple et robuste : Le deck d'export doit essayer d'utiliser les vrais noms configurés s'ils sont disponibles, puis appeler `CardResolver(zip_path).resolve()`.
- Le chemin du zip est `/data/cache/aggregate.zip` (à localiser proprement via `Path`).

### Architecture Compliance
- Garder `CardResolver` dans son rôle : il prend des strings, il sort des ints.
- Ne pas ralentir l'audit si l'utilisateur ne demande pas l'exportation.

### File Structure Requirements
- **MODIFIED** `src/ygo_ultime_deck/main.py` : L'appel au resolver.

### Testing Requirements
- Exécuter la commande `audit` manuellement et vérifier le contenu du fichier `output.ydk` généré pour s'assurer que les Mock IDs sont présents (pour les noms génériques) ET que d'éventuels vrais noms donneraient un vrai ID.

## Tasks / Subtasks
- [x] Modifier `main.py` pour instancier `CardResolver`.
- [x] Construire une liste de noms à résoudre (ex: utiliser les noms du YAML, ou fallback sur "Starter", etc.).
- [x] Remplacer les IDs codés en dur par `resolver.resolve(names)`.

## Dev Agent Record
- **Implementation Notes:** J'ai modifié `main.py` pour instancier `CardResolver` juste avant l'exportation. Le script parse d'abord le fichier YAML de requêtes pour en extraire tous les noms uniques utilisés dans les combos. Il complète ensuite la decklist jusqu'à `opt_size` (40) avec le nom "Generic Card". Enfin, il appelle le resolver pour convertir cette liste de noms en IDs, qu'il insère dans le YDK.
- **Tests Added:** Aucun test unitaire supplémentaire car le resolver est testé dans `test_resolver.py` et la génération YDK dans `test_exporter.py`. L'intégration a été testée avec la commande `uv run ygo-deck audit` qui génère correctement la liste d'IDs mock (puisque "Generic Card" n'existe pas).

### File List
- `src/ygo_ultime_deck/main.py`

## Change Log
- Modification de `src/ygo_ultime_deck/main.py` pour inclure l'appel à `CardResolver` dans la commande `audit`.

## Completion Status
- **Status Update:** review
- **Note:** Initial story definition completed.

## Code Review Findings
**Severity Breakdown:** 2 High | 4 Medium | 4 Low

### Action Items
- [ ] [AI-Review][High] Deduplication alters quantities: Extract names with their counts instead of deduplicating them.
- [ ] [AI-Review][Medium] Omission of Unit Tests: Refactor name extraction and add tests.
- [ ] [AI-Review][Low] Unconditional execution: Ensure CardResolver is only called if output generation succeeds/is needed.
- [ ] [AI-Review][Low] Missed `--core` fallback: Update `--core` to accept a string name instead of an int.
- [ ] [AI-Review][High] Path Fragility: Fix `cache_path` resolution.
- [ ] [AI-Review][Medium] Potential Iteration Crash: Handle `None` for combos/requirements safely.
- [ ] [AI-Review][Medium] O(N^2) Uniqueness Check: (Superseded by fixing deduplication)
- [ ] [AI-Review][Low] Silent Truncation: Add a `logger.warning`.
- [ ] [AI-Review][Low] Inline Imports: Move `CardResolver` import to module top.
- [ ] [AI-Review][Low] Untracked Generated Artifacts: Add `output/` to `.gitignore`.
