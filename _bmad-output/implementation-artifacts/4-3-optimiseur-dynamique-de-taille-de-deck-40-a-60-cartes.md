---
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
- [ ] Implémenter la fonction d'optimisation (balayage de 40 à 60).
- [ ] Intégrer les calculs de probabilités hypergéométriques pour l'optimum.
- [ ] Ajouter les tests unitaires pour valider les résultats avec des configurations connues.

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
