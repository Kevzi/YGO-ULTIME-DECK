---
stepsCompleted: [1, 2, 3]
inputDocuments: ["prd.md", "architecture.md"]
---

# YGO ULTIME DECK - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for YGO ULTIME DECK, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

FR1: Ingestion YGOJSON via l'archive `aggregate.zip` (schéma v0.6.0).
FR2: Mise en cache locale avec une commande CLI dédiée `--update` pour les performances.
FR3: Parseur résilient gérant les champs manquants, les monstres normaux sans effet, et le formatage générique.
FR4: Catégorisation sémantique avec un moteur Regex basé sur le format de texte Konami (PSCT).
FR5: Multi-Tagging Dynamique pour tester différents rôles lors des simulations de combos.
FR6: Règles sémantiques isolées dans un fichier externe modifiable `config/tags_rules.yaml`.
FR7: Moteur Mathématique hypergéométrique et Monte-Carlo configuré via `config/target_combos.yaml`.
FR8: Résolution native des "Resource Generators" (creusage dynamique et pioche) dans le calcul des probabilités.
FR9: Intelligence de Counter-Matching basée sur un fichier externe `config/meta_targets.yaml`.
FR10: Logique d'Immunité avec simulation de l'archétype sous l'effet de la carte contre (visant 100% de réussite).
FR11: Audit de deck et Exportation du résultat final au format standard `.ydk`.
FR12: Taille de Deck Dynamique optimisée (de 40 à 60 cartes) justifiée mathématiquement par la dilution des briques (Garnets) avec un ratio de Starters > 85%.

### NonFunctional Requirements

NFR1: Performance : Le SLA autorise un traitement asynchrone de 15 à 30 secondes pour les simulations Monte-Carlo (100 000 itérations).
NFR2: Optimisation RAM : Pré-filtrage strict des données à la mise en cache pour éliminer la banlist et les formats alternatifs (Rush Duel, etc.).
NFR3: Sécurité Mémoire : Implémentation de l'algorithme logarithmique anti-overflow (`math.lgamma`) pour les factoriels géants.

### Additional Requirements

- Projet initié avec la commande `uv init --package ygo_ultime_deck`, `Typer` et `Pydantic` (Important for Epic 1 Story 1).
- Flux de données strictement unidirectionnel via pipeline Pydantic (Data Flow).
- Orchestration hybride asynchrone avec `asyncio` pour la CLI et `ProcessPoolExecutor` pour la boucle mathématique (Multiprocessing).
- Gestion d'erreur globale via `Typer` et `Rich` pour éviter les stacktraces brutes (`typer.Exit(1)`).
- Formatage et linting stricts du code avec `Ruff` et tests avec `pytest`.
- Structure de modules stricte dans `src/ygo_ultime_deck/` (`ingestion/`, `rules/`, `engine/`, `intelligence/`, `models/`).

### UX Design Requirements

N/A

### FR Coverage Map

- FR1: Epic 1 - Ingestion YGOJSON `aggregate.zip`
- FR2: Epic 1 - Commande CLI `--update` pour cache local
- FR3: Epic 1 - Parseur résilient et pré-filtrage RAM
- FR4: Epic 2 - Catégorisation sémantique Regex
- FR5: Epic 2 - Multi-Tagging Dynamique
- FR6: Epic 2 - Règles sémantiques isolées dans YAML
- FR7: Epic 3 - Moteur Mathématique & Input YAML (`target_combos.yaml`)
- FR8: Epic 3 - Résolution native des "Resource Generators" (effets de pioche)
- FR9: Epic 4 - Intelligence Counter-Matching (`meta_targets.yaml`)
- FR10: Epic 4 - Logique d'Immunité (simulation sous effets de contre)
- FR11: Epic 4 - Audit et Exportation standard `.ydk`
- FR12: Epic 4 - Taille de Deck Dynamique optimisée (40 à 60 cartes)

## Epic List

### Epic 1: Initialisation et Synchronisation de la Base de Données YGO
L'utilisateur peut initialiser le projet CLI et maintenir une base de données Yu-Gi-Oh! locale, ultra-rapide et optimisée, prête pour l'analyse algorithmique sans dépendre du réseau.
**FRs covered:** FR1, FR2, FR3.

### Epic 2: Personnalisation et Auto-Tagging Sémantique
L'utilisateur peut dicter ses propres règles de mots-clés via un fichier YAML pour que l'outil catégorise intelligemment le rôle de chaque carte (Starter, Extender) grâce aux Regex.
**FRs covered:** FR4, FR5, FR6.

### Epic 3: Simulateur de Combos et Analyse Mathématique
L'utilisateur peut définir ses "mains de rêve" et obtenir instantanément les probabilités d'ouverture fiables via le moteur de Monte-Carlo et l'algorithme hypergéométrique.
**FRs covered:** FR7, FR8.

### Epic 4: Génération de la "Decklist Ultime" et Exportation YDK
L'utilisateur reçoit une decklist prête à jouer (.ydk) mathématiquement optimisée en taille (40-60 cartes) et prouvée virtuellement immunisée contre les meilleurs decks du format.
**FRs covered:** FR9, FR10, FR11, FR12.

## Epic 1: Initialisation et Synchronisation de la Base de Données YGO

L'utilisateur peut initialiser le projet CLI et maintenir une base de données Yu-Gi-Oh! locale, ultra-rapide et optimisée, prête pour l'analyse algorithmique sans dépendre du réseau.

### Story 1.1: Initialisation du Projet & Socle CLI (Typer)

As a développeur / utilisateur CLI,
I want initialiser la structure du projet avec `uv`, `Typer` et `Rich`,
So that je puisse exécuter la commande globale `ygo-deck --help` et obtenir une interface propre et professionnelle.

**Acceptance Criteria:**

**Given** l'environnement de développement vide
**When** le développeur lance `uv init --package ygo_ultime_deck` et configure `pyproject.toml`
**Then** le point d'entrée `ygo-deck` est disponible globalement
**And** l'exécution de la commande affiche le menu d'aide standard formaté par `Rich` sans aucune erreur (Code de sortie 0).

### Story 1.2: Modèles de Données Pydantic (Schéma v0.6.0)

As a système de traitement,
I want disposer de modèles Pydantic stricts (`CardModel`) basés sur le schéma YGOJSON,
So that les données transitent dans le pipeline sous forme d'objets purs, garantissant le "Thread-Safety" pour le multiprocessing.

**Acceptance Criteria:**

**Given** les spécifications du schéma YGOJSON v0.6.0
**When** le système instancie une carte (y compris avec des champs manquants comme `series` ou un type "Mot-clé" réservé en Python)
**Then** Pydantic valide les données via `Field(alias="type")`
**And** l'objet généré est 100% sérialisable (Picklable) sans aucun état persistant.

### Story 1.3: Téléchargeur YGOJSON (Gestion du Cache)

As a utilisateur CLI,
I want pouvoir utiliser une commande `ygo-deck --update`,
So that le système télécharge de manière asynchrone l'archive `aggregate.zip` depuis YGOJSON et la stocke dans le dossier local `/data/cache/`.

**Acceptance Criteria:**

**Given** une connexion internet active
**When** l'utilisateur exécute `ygo-deck --update`
**Then** l'application affiche une barre de progression `Rich`
**And** le fichier `aggregate.zip` est téléchargé et sauvegardé correctement dans le cache local
**And** si le réseau coupe, une erreur élégante est affichée via `typer.Exit(1)` au lieu d'une stacktrace brute.

### Story 1.4: Parseur Résilient & Pré-filtrage Mémoire

As a moteur d'ingestion,
I want décompresser le cache local et parser les cartes tout en ignorant les cartes illégales (Rush Duel, Banlist),
So that la RAM ne soit chargée qu'avec les cartes compétitives pertinentes, évitant les crashs sur des champs manquants (ex: Monstres Normaux).

**Acceptance Criteria:**

**Given** le cache local `aggregate.zip` téléchargé
**When** l'application initialise le pipeline de données
**Then** elle extrait le JSON, ignore les cartes n'ayant pas le format "TCG" ou "OCG"
**And** elle transforme chaque carte valide en `CardModel`
**And** la fonction retourne la liste des modèles sans crasher, même face aux monstres normaux (qui n'ont pas de texte d'effet complexe).

## Epic 2: Personnalisation et Auto-Tagging Sémantique

L'utilisateur peut dicter ses propres règles de mots-clés via un fichier YAML pour que l'outil catégorise intelligemment le rôle de chaque carte (Starter, Extender) grâce aux Regex.

### Story 2.1: Moteur d'Expressions Régulières (Regex PSCT)

As a moteur de catégorisation,
I want utiliser des expressions régulières (Regex) pré-compilées pour scanner les textes d'effets des cartes,
So that l'identification des mécaniques de jeu (ex: "Add 1 card", "Special Summon") soit quasi-instantanée et ne dépende pas d'une intelligence artificielle (NLP) lourde.

**Acceptance Criteria:**

**Given** un objet `CardModel` contenant un texte d'effet de type PSCT
**When** la fonction de tagging sémantique scanne la description
**Then** l'algorithme fait correspondre le texte avec les Regex sans crash (même sur des textes très longs ou complexes)
**And** attribue le tag adéquat dans un temps de calcul minimal.

### Story 2.2: Fichier de Configuration Externe (`tags_rules.yaml`)

As a concepteur de deck (utilisateur avancé),
I want définir le dictionnaire liant les mots-clés aux "Tags" dans un fichier `config/tags_rules.yaml`,
So that je puisse modifier l'intelligence du système ou ajouter de nouvelles règles sans jamais avoir à retoucher le code source Python.

**Acceptance Criteria:**

**Given** un fichier `tags_rules.yaml` défini par l'utilisateur
**When** le système initialise l'Epic 2
**Then** l'application charge ce fichier de manière sécurisée (gestion de `FileNotFoundError` avec Typer)
**And** injecte ces règles dynamiquement dans le Moteur Regex.

### Story 2.3: Implémentation du Multi-Tagging Dynamique

As a simulateur de combos (Moteur Mathématique),
I want que les cartes puissent recevoir une liste de rôles au lieu d'un rôle unique (ex: `[Starter, Extender]`),
So that je puisse tester virtuellement tous ces rôles en fonction des autres cartes en main pour trouver le combo optimal.

**Acceptance Criteria:**

**Given** une carte dont l'effet match plusieurs règles Regex différentes
**When** le moteur de tagging a fini son traitement
**Then** l'attribut `CardModel.tags` contient une liste Python native de tous les tags validés
**And** la liste ne contient aucun doublon.

## Epic 3: Simulateur de Combos et Analyse Mathématique

L'utilisateur peut définir ses "mains de rêve" et obtenir instantanément les probabilités d'ouverture fiables via le moteur de Monte-Carlo et l'algorithme hypergéométrique.

### Story 3.1: Algorithme Hypergéométrique Logarithmique

As a moteur mathématique,
I want calculer les probabilités de tirage via un algorithme logarithmique (ex: `math.lgamma`),
So that le système ne crashe jamais sur une erreur de dépassement de mémoire ("overflow") lors du calcul de factoriels massifs (ex: factorielle de 60).

**Acceptance Criteria:**

**Given** un calcul de probabilité complexe sur un deck de 60 cartes
**When** la fonction `calculate_hypergeometric` est appelée
**Then** l'algorithme utilise les logarithmes pour neutraliser le risque d'overflow
**And** retourne la probabilité mathématiquement exacte (float) pour une main statique.

### Story 3.2: Parseur des "Mains de Rêve" (`target_combos.yaml`)

As a concepteur de deck (utilisateur CLI),
I want définir les cartes ou les tags requis pour un combo réussi (ex: 1 Starter + 1 Extender) dans un fichier `config/target_combos.yaml`,
So that je n'aie pas à écrire des arguments CLI complexes dans le terminal pour tester mes stratégies.

**Acceptance Criteria:**

**Given** un fichier `target_combos.yaml` contenant plusieurs scénarios (Combo A, Combo B)
**When** la simulation démarre
**Then** le système valide la syntaxe et convertit les requêtes en objets Pydantic (ex: `SimulationRequest`)
**And** transmet ces paramètres proprement au moteur mathématique.

### Story 3.3: Moteur de Simulation Monte-Carlo (Multiprocessing)

As a orchestrateur de performance,
I want distribuer la force brute de calcul (100 000 itérations de mains aléatoires, Tour 1 et Tour 2) via un pool de processus natif (`ProcessPoolExecutor`),
So that le SLA de 15 à 30 secondes soit scrupuleusement respecté sans jamais bloquer l'interface utilisateur.

**Acceptance Criteria:**

**Given** une simulation exigeant 100 000 mains virtuelles
**When** la commande est lancée
**Then** le système divise les itérations en lots (chunks) répartis sur les cœurs du CPU (Worker processes)
**And** la boucle `asyncio` principale reste réactive et affiche la progression sur le terminal
**And** le calcul est accompli et agrégé en moins de 30 secondes.

### Story 3.4: Résolution des "Resource Generators" (Pioche Dynamique)

As a analyseur de combo,
I want que le simulateur exécute virtuellement l'effet des cartes de pioche (ex: "Excavate-6" d'un *Pot de Prospérité*),
So that l'analyse reflète la vraie probabilité de trouver un combo en creusant dans le deck, et pas seulement avec les 5 cartes de départ statiques.

**Acceptance Criteria:**

**Given** une main de départ simulée contenant une carte taguée comme ressource (ex: `Draw-2` ou `Excavate-6`)
**When** l'évaluation du combo échoue sur les 5 premières cartes
**Then** le moteur simule le fait de piocher/creuser dans le reste du deck virtuel
**And** recalcule si le combo est finalement atteint avec ces nouvelles cartes.

## Epic 4: Génération de la "Decklist Ultime" et Exportation YDK

L'utilisateur reçoit une decklist prête à jouer (.ydk) mathématiquement optimisée en taille (40-60 cartes) et prouvée virtuellement immunisée contre les meilleurs decks du format.

### Story 4.1: Parseur des Menaces de la Méta (`meta_targets.yaml`)

As a utilisateur CLI,
I want définir les "staples" (cartes génériques jouées par l'adversaire) et les decks méta dans un fichier `config/meta_targets.yaml`,
So that le système connaisse les interruptions majeures contre lesquelles il doit tester l'immunité de mes combos.

**Acceptance Criteria:**

**Given** un fichier `meta_targets.yaml` contenant des menaces comme "Ash Blossom" ou "Nibiru"
**When** l'analyse de méta démarre
**Then** l'outil parse ces menaces et prépare une liste d'interruptions virtuelles à injecter dans le moteur de simulation.

### Story 4.2: Simulation de l'Immunité (Counter-Matching)

As a moteur d'intelligence,
I want simuler l'effet des cartes "Contre" adverses sur ma main testée,
So that je puisse déterminer si le combo survit et atteint tout de même son objectif, prouvant ainsi son "Immunité" (visant 100% de réussite malgré l'interruption).

**Acceptance Criteria:**

**Given** un combo identifié comme réussi par le simulateur de base (Epic 3)
**When** le module d'intelligence injecte virtuellement une menace
**Then** l'algorithme vérifie si la main possède des cartes de protection (ex: "Called by the Grave") ou assez d'Extenders pour continuer de jouer
**And** marque le test d'immunité comme Succès ou Échec.

### Story 4.3: Optimiseur Dynamique de Taille de Deck (40 à 60 cartes)

As a constructeur de deck automatique,
I want calculer le ratio optimal entre les Starters et les Garnets (briques) pour toutes les tailles de deck de 40 à 60 cartes,
So that l'algorithme puisse justifier mathématiquement d'augmenter la taille du deck si cela dilue les Garnets tout en conservant une consistance de Starters > 85%.

**Acceptance Criteria:**

**Given** un noyau de deck (Core Engine) et une liste de "Garnets" injouables
**When** la fonction d'optimisation de ratio est appelée
**Then** elle simule les probabilités hypergéométriques pour 40, 41, 42... jusqu'à 60 cartes
**And** sélectionne la taille exacte offrant le meilleur compromis (Dilution maximale des Garnets + > 85% d'ouverture du Starter).

### Story 4.4: Module d'Audit CLI et Exportation `.ydk`

As a joueur Yu-Gi-Oh!,
I want que l'application génère un rapport final élégant résumant les probabilités et exporte la "Decklist Ultime" dans un fichier `.ydk`,
So that je puisse lire les statistiques dans mon terminal et importer le deck directement dans un simulateur comme Omega ou Edopro pour jouer.

**Acceptance Criteria:**

**Given** qu'une taille de deck optimale et une liste de cartes finalisée ont été calculées
**When** la chaîne de calcul globale se termine
**Then** un tableau de statistiques esthétique est généré via `Rich` (affichant pourcentages de combos et d'immunité)
**And** un fichier au format standard `.ydk` (contenant les IDs officiels des cartes) est créé dans le dossier de sortie.
