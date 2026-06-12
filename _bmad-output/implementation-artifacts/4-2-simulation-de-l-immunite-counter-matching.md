---
# Story 4.2: Simulation de l'Immunité (Counter-Matching)

**Status:** ready-for-dev
**Epic:** 4 - Génération de la "Decklist Ultime" et Exportation YDK

## Story Requirements

**User Story:**
As a moteur d'intelligence,
I want simuler l'effet des cartes "Contre" adverses sur ma main testée,
So that je puisse déterminer si le combo survit et atteint tout de même son objectif, prouvant ainsi son "Immunité" (visant 100% de réussite malgré l'interruption).

**Acceptance Criteria:**
- **Given** un combo identifié comme réussi par le simulateur de base (Epic 3)
- **When** le module d'intelligence injecte virtuellement une menace
- **Then** l'algorithme vérifie si la main possède des cartes de protection (ex: "Called by the Grave") ou assez d'Extenders pour continuer de jouer
- **And** marque le test d'immunité comme Succès ou Échec.

## Developer Context & Guardrails

### Technical Requirements
- Mettre à jour le moteur de simulation (ou créer un module d'immunité spécifique) pour intégrer la logique de "Counter-Matching".
- Si une menace est injectée (ex: "Handtrap"), le système doit vérifier si la main de départ contient une carte avec le tag "Protection" (ou anti-handtrap). Si oui, la menace est neutralisée et le combo passe.
- S'il n'y a pas de protection, le système doit retirer un "Starter" ou un "Extender" (selon la menace) et réévaluer si les conditions du `TargetCombo` sont toujours satisfaites avec le reste de la main.
- Les résultats doivent être remontés dans `SimulationResult` sous forme de métriques d'immunité (ex: `immunity_success_rate`).

### Architecture Compliance
- Ne pas casser le moteur de Monte-Carlo (Epic 3). La logique d'immunité doit s'exécuter soit post-validation du combo, soit en parallèle.
- S'appuyer sur la structure de données `MetaThreat` développée dans la Story 4.1.
- Conserver la haute performance du multiprocessing (Worker).

### File Structure Requirements
- **MODIFY** `src/ygo_ultime_deck/engine/worker.py` : Ajouter la logique d'évaluation de l'immunité après le tirage.
- **MODIFY** `src/ygo_ultime_deck/models/simulation.py` : Ajouter les champs pour les résultats d'immunité.
- **NEW/MODIFY** `tests/test_engine/test_immunity.py` : Tests unitaires de la logique de résilience aux menaces.

### Testing Requirements
- Test où la main a une protection : l'interruption échoue, combo réussi.
- Test où la main n'a pas de protection mais trop d'extenders : l'interruption détruit 1 carte, mais le combo passe quand même.
- Test où la main n'a ni protection ni extenders supplémentaires : l'interruption détruit le combo, échec.

## Tasks / Subtasks
- [ ] Étendre le modèle `SimulationResult` pour inclure les statistiques d'immunité.
- [ ] Implémenter la logique `evaluate_immunity` dans le worker (neutralisation par "Protection" ou "Extender").
- [ ] Intégrer l'évaluation de l'immunité dans la boucle de simulation principale de Monte-Carlo.
- [ ] Écrire les tests unitaires pour garantir la justesse mathématique du contre.

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
