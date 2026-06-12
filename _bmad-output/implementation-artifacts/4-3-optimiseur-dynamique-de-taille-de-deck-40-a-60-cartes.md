---
baseline_commit: 960f0b0d23006248bf135960e22b63bb6a0e271e
# Story 4.3: Optimiseur Dynamique de Taille de Deck (40 à 60 cartes)

**Status:** ready-for-dev
**Epic:** 4 - Génération de la "Decklist Ultime" et Exportation YDK

## Story Requirements

**User Story:**
As a constructeur de deck automatique,
I want calculer le ratio optimal entre les Starters et les Garnets (briques) pour toutes les tailles de deck de 40 à 60 cartes,
So that l'algorithme puisse justifier mathématiquement d'augmenter la taille du deck si cela dilue les Garnets tout en conservant une consistance de Starters > 85%.

**Acceptance Criteria:**
- **Given** un noyau de deck (Core Engine) et une liste de "Garnets" injouables
- **When** la fonction d'optimisation de ratio est appelée
- **Then** elle simule les probabilités hypergéométriques pour 40, 41, 42... jusqu'à 60 cartes
- **And** sélectionne la taille exacte offrant le meilleur compromis (Dilution maximale des Garnets + > 85% d'ouverture du Starter).

## Developer Context & Guardrails

### Technical Requirements
- Créer un module d'optimisation (ex: `src/ygo_ultime_deck/engine/optimizer.py`).
- Utiliser la fonction hypergéométrique existante de l'Epic 3 pour simuler la probabilité de piocher au moins 1 Starter.
- Utiliser la fonction hypergéométrique pour simuler la probabilité de piocher 0 Garnets.
- Définir une fonction de coût (score) : maximiser la probabilité de piocher le Starter tout en minimisant la probabilité de piocher le Garnet.
- La taille de deck optimale est celle qui maximise ce score combiné, sous contrainte que `P(Starter) >= 0.85` (ou la meilleure possible si le deck ne peut pas atteindre 85%).
- Le reste des cartes (40-60 moins le Core Engine et les Garnets) est supposé être rempli par des "Staples" (Cartes génériques/Handtraps).

### Architecture Compliance
- Ce module doit être purement mathématique (rapide).
- Doit utiliser `calculate_hypergeometric` implémentée dans `math_utils.py` (ou `monte_carlo.py` si c'est de l'hypergéométrique). Wait, l'Epic 3 a demandé "Algorithme Hypergéométrique Logarithmique", donc il doit y avoir une fonction mathématique disponible.
- Séparer la logique métier pure du CLI.

### File Structure Requirements
- **NEW** `src/ygo_ultime_deck/engine/optimizer.py` : Logique de l'optimiseur.
- **NEW** `tests/test_engine/test_optimizer.py` : Tests unitaires.

### Testing Requirements
- Test où 40 cartes est l'optimum (très peu de garnets).
- Test où 60 cartes est l'optimum (beaucoup de garnets, énormément de starters).
- Test où la contrainte des 85% force une taille de deck spécifique.

## Tasks / Subtasks
- [x] Implémenter la fonction d'optimisation (balayage de 40 à 60).
- [x] Intégrer les calculs de probabilités hypergéométriques pour l'optimum.
- [x] Ajouter les tests unitaires pour valider les résultats avec des configurations connues.

## Dev Agent Record
- **Implementation Notes:** L'optimiseur utilise l'algorithme hypergéométrique de l'Epic 3 pour simuler 21 tailles de deck (40 à 60). Il calcule P(Starter >= 1) et P(Garnet == 0). Si un deck atteint les 85% de Starter, il sélectionne celui qui a le moins de Garnets. S'il n'y a pas de Garnet, il favorise toujours le plus petit deck. La fonction est `O(n)` sur la plage de deck (donc 21 itérations) et est instantanée.
- **Tests Added:** `tests/test_engine/test_optimizer.py` avec 5 tests vérifiant les extrêmes (0 garnet = 40 cartes, beaucoup de garnets = > 40 cartes, fallback consistency = 40, core size override, max size exception).

### File List
- `src/ygo_ultime_deck/engine/optimizer.py` (NEW)
- `tests/test_engine/test_optimizer.py` (NEW)

## Change Log
- Ajout du module `optimizer.py` capable de calculer mathématiquement la taille idéale d'un deck selon le ratio Starter/Garnet.

## Completion Status
- **Status Update:** done
- **Note:** Initial story definition completed.

## Code Review Findings
**Severity Breakdown:** 4 High | 3 Medium | 1 Low

### Action Items
- [x] [AI-Review][High] Incorrect Optimization Target: The code uses `max(valid_sizes, key=lambda x: (x["p_no_garnet"], x["score"]))` which maximizes `p_no_garnet` as the primary key. Fix: Maximize `x["score"]` directly.
- [x] [AI-Review][High] Missing Input Validation (Empty Range Crash): If `min_deck > max_deck`, the loop is skipped and `results` is empty, causing `max(results)` to crash. Fix: Raise ValueError if min > max.
- [x] [AI-Review][High] Missing Input Validation (Impossible Decks): No validation for negative inputs or if `starters_count + garnets_count > deck_size`. Fix: Add guards for these conditions.
- [x] [AI-Review][High] Statistically Invalid Scoring Logic (Heuristic Flaw): `score = p_starter * p_no_garnet` naively multiplies two dependent events. Fix: Document this as a heuristic scoring function rather than a true probability.
- [x] [AI-Review][Medium] Flawed Fallback Logic: If no deck size reaches the `starter_threshold`, the function falls back to the max combined score which could dilute starters too much. Fix: Fallback to the maximum `p_starter` to preserve consistency.
- [x] [AI-Review][Medium] Misleading Error Messaging: The `ValueError` explicitly blames `Core Engine` if `actual_min > max_deck`. Fix: Improve error message accuracy.
- [x] [AI-Review][Medium] Incomplete Test Coverage: Add a test where a specific size crosses the 85% threshold, forcing that size to be chosen.
- [x] [AI-Review][Low] Zero Starters Edge Case: If `starters_count == 0`, it fails silently. Fix: Raise ValueError.
