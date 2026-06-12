---
# Story 4.4: Module d'Audit CLI et Exportation `.ydk`

**Status:** ready-for-dev
**Epic:** 4 - Génération de la "Decklist Ultime" et Exportation YDK

## Story Requirements

**User Story:**
As a joueur Yu-Gi-Oh!,
I want que l'application génère un rapport final élégant résumant les probabilités et exporte la "Decklist Ultime" dans un fichier `.ydk`,
So that je puisse lire les statistiques dans mon terminal et importer le deck directement dans un simulateur comme Omega ou Edopro pour jouer.

**Acceptance Criteria:**
- **Given** qu'une taille de deck optimale et une liste de cartes finalisée ont été calculées
- **When** la chaîne de calcul globale se termine
- **Then** un tableau de statistiques esthétique est généré via `Rich` (affichant pourcentages de combos et d'immunité)
- **And** un fichier au format standard `.ydk` (contenant les IDs officiels des cartes) est créé dans le dossier de sortie.

## Developer Context & Guardrails

### Technical Requirements
- Créer un module d'exportation `src/ygo_ultime_deck/engine/exporter.py` ou équivalent.
- Le module doit accepter une liste de `CardModel` (ou d'IDs) pour le Main Deck, Extra Deck et Side Deck.
- Format `.ydk`:
  ```
  #created by ...
  #main
  ID_1
  ID_2
  #extra
  ID_3
  !side
  ID_4
  ```
- Créer une commande CLI (ou l'intégrer à la commande principale) qui consolide les informations: `SimulationResult` + `optimizer result`.
- Utiliser la librairie `rich.table` et `rich.console` pour afficher un rapport final spectaculaire.

### Architecture Compliance
- Typer pour l'interface CLI.
- Le fichier `.ydk` doit être sauvegardé dans un dossier défini, par exemple `output/decklist_ultime.ydk`.

### File Structure Requirements
- **NEW/MODIFIED** `src/ygo_ultime_deck/cli.py` : Intégration du rapport riche.
- **NEW** `src/ygo_ultime_deck/engine/exporter.py` : Logique d'écriture du YDK.
- **NEW** `tests/test_engine/test_exporter.py` : Tests unitaires.

### Testing Requirements
- Test garantissant que le format `.ydk` est valide et contient bien les sections `#main`, `#extra`, `!side`.
- Test sur la gestion des dossiers de sortie (ex: création automatique si manquant).

## Tasks / Subtasks
- [ ] Créer la fonction d'exportation `generate_ydk(decklist, filepath)`.
- [ ] Concevoir le tableau récapitulatif avec `Rich` (taux de réussite, immunités, ratio starters/garnets).
- [ ] Intégrer l'exportation et l'affichage dans le workflow global CLI.
- [ ] Ajouter les tests unitaires.

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
