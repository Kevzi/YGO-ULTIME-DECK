---
baseline_commit: b9b9b195fd5c5651ca70c6390f61ff64a3f9f36c
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
- [x] Étendre le modèle `SimulationResult` pour inclure les statistiques d'immunité.
- [x] Implémenter la logique `evaluate_immunity` dans le worker (neutralisation par "Protection" ou "Extender").
- [x] Intégrer l'évaluation de l'immunité dans la boucle de simulation principale de Monte-Carlo.
- [x] Écrire les tests unitaires pour garantir la justesse mathématique du contre.

## Dev Agent Record
- **Implementation Notes:** L'immunité est implémentée de manière extrêmement optimisée. Le worker évalue mathématiquement si une carte peut être sacrifiée aux interruptions. Si `hand_counts.get("Protection", 0) > 0`, l'interruption est annulée. Sinon, le script vérifie s'il existe une redondance pour TOUS les prérequis du combo. Si oui, le combo passe malgré l'interruption. `SimulationResult` a été étendu pour accumuler les succès avec interruptions séparément (`immunity_success_rates`).
- **Tests Added:** Ajout de `test_immunity.py` avec 4 tests complets validant la protection, les extenders, l'échec total et la fonction de wrapping `simulate_chunk`. Les tests de `monte_carlo.py` ont été validés avec la nouvelle intégration.

### File List
- `src/ygo_ultime_deck/engine/worker.py` (MODIFIED)
- `src/ygo_ultime_deck/models/simulation.py` (MODIFIED)
- `src/ygo_ultime_deck/engine/monte_carlo.py` (MODIFIED)
- `tests/test_engine/test_immunity.py` (NEW)

## Change Log
- Ajout de la simulation de l'immunité (Counter-Matching) dans le moteur de Monte-Carlo.

## Completion Status
- **Status Update:** done
- **Note:** Initial story definition completed.

## Code Review Findings
**Severity Breakdown:** 3 High | 1 Medium | 2 Low

### Action Items
- [x] [AI-Review][High] Flawed Domain Logic (Overly Pessimistic): `evaluate_immunity` fails the combo if *any* requirement lacks an extender (`if hand_counts.get(req_name, 0) <= req_count: return False`). While this correctly models an opponent with perfect knowledge playing optimally to break the combo, it assumes the threat can target *any* card. In reality, specific threats (like Ash Blossom) only hit specific types of cards. Fix: Use the `threat["category"]` to determine the logic (e.g. Handtraps destroy Starters).
- [x] [AI-Review][High] Ignored Threat Characteristics: `evaluate_immunity` accepts a `threat` dictionary but ignores its `category`.
- [x] [AI-Review][High] Invalid Simulation Timing for Draw Combos: In `simulate_chunk`, immunity is evaluated *after* draw and excavate effects have been resolved. Realistically, threats like Ash Blossom respond to the draw effect itself.
- [x] [AI-Review][Medium] Unsafe Dictionary Aggregation: In `run_monte_carlo_simulation`, the code blindly increments `total_result.immunity_success_rates[combo_name][threat_name] += successes`. This can throw an unhandled `KeyError`. Fix: Use `setdefault`.
- [x] [AI-Review][Low] Missing `name` key crash: If a threat dictionary lacks a `"name"` key, it will crash the initialization of the dictionaries. Fix: Use `t.get('name', 'Unknown')`.
- [x] [AI-Review][Low] Sloppy Initialization / Performance: `immunity_successes` is assigned empty dicts, then mutated. Also, `evaluate_immunity` is a function call in the hottest loop. Fix: Inline logic and optimize dictionary comprehensions.
