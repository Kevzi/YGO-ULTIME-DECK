---
title: YGO ULTIME DECK - PRD
status: final
created: 2026-06-09
updated: 2026-06-09
---

# YGO ULTIME DECK - Product Requirements Document

## 1. Vue d'ensemble du produit
L'objectif de cette V1 est de fournir un moteur backend (script Python/CLI) capable de générer des decks Yu-Gi-Oh! optimisés (Anti-Méta) en combinant analyse sémantique et distribution hypergéométrique multivariée, offrant ainsi un avantage compétitif mesurable en tournoi.

## 2. Fonctionnalités & Capacités (Features)

### F1. Ingestion et Traitement de Données (YGOJSON)
- **Source** : `aggregate.zip` depuis YGOJSON (schéma v0.6.0).
- **Mise en cache locale (Performance)** : Le système ne télécharge pas les données à chaque exécution. Une commande dédiée (ex: `--update`) télécharge et met en cache la base localement pour assurer une génération instantanée.
- **Résilience (Edge Cases)** : Le parseur ne crashe jamais sur des champs manquants. Une carte sans `series` est classée "Générique". Les Monstres Normaux (sans effets) sont conservés en mémoire et peuvent recevoir le tag "Garnet" si nécessaires à des combos.
- **Pré-filtrage strict (Optimisation RAM)** : Au moment de la mise en cache, l'algorithme utilise le champ `formats` pour écarter de la RAM toutes les cartes bannies par la banlist actuelle ainsi que les cartes exclusives aux formats alternatifs (Rush Duel, Speed Skills).

### F2. Catégorisation Fonctionnelle (Auto-Tagging)
- **Parseur Sémantique (Regex)** : L'algorithme se base sur le format PSCT (Problem-Solving Card Text) de Konami. Il utilise des expressions régulières (Regex) légères et rapides pour repérer les effets clés (ex: "Add 1 card" = Starter), évitant la lourdeur d'un modèle d'Intelligence Artificielle (NLP).
- **Multi-Tagging Dynamique** : Le système supporte les rôles multiples (ex: une carte peut être taguée `[Starter, Extender]`). Lors de la simulation des combos, le moteur mathématique teste les combinaisons et assigne dynamiquement le rôle optimal à la carte en fonction des autres cartes en main.
- **Évolutivité (Fichier de Configuration Externe)** : Toutes les règles sémantiques (dictionnaire de mots-clés liant les textes aux tags) sont stockées dans un fichier de configuration externe modifiable par l'utilisateur (`tags_rules.yaml` ou `.json`). Le script Python ne fait que lire ce fichier, permettant une mise à jour facile lors des futures extensions sans modifier le code source.

### F3. Moteur Mathématique (Calculateur Hypergéométrique)
- **SLA de Performance (Précision > Vitesse)** : Le moteur utilise un algorithme logarithmique anti-overflow pour les calculs purs. Pour la résolution complexe des mains (multi-tagging, effets de pioche), il utilise une simulation de Monte-Carlo à haute fidélité (jusqu'à 100 000 itérations). Un délai de traitement de 15 à 30 secondes est explicitement accepté pour garantir une précision absolue.
- **Input Utilisateur (`target_combos.yaml`)** : L'utilisateur définit ses critères de succès (les "mains de rêve" à maximiser) via un fichier YAML dédié, évitant une syntaxe CLI complexe et préparant le terrain pour l'API JSON de la future V2 Web.
- **Périmètre de Simulation Exhaustif** : Le moteur calcule simultanément les probabilités pour le Tour 1 (main de 5 cartes) et le Tour 2 (main de 6 cartes). Il gère nativement la résolution des "Resource Generators" (ex: simulation de la pioche ou du creusage dans le deck après l'activation d'un *Pot de Prospérité*) pour mettre à jour les probabilités dynamiquement.

### F4. Intelligence de Counter-Matching et Génération (Le "Moat")
- **Input de la Méta (`meta_targets.yaml`)** : Le système ne hardcode aucune "Méta". L'utilisateur indique les decks dominants et leurs points d'étranglement sémantiques dans un fichier YAML (ex: DoomZ = vulnérable au bannissement).
- **Logique d'Immunité (Déduction par Simulation)** : L'IA ne se base pas sur de simples tags pour choisir son propre deck. Elle prouve l'immunité en simulant virtuellement les combos des archétypes sous l'effet de la carte de contre sélectionnée (ex: Dimension Shifter). Si la simulation réussit à 100%, l'archétype est sélectionné.
- **Audit et Exportation (Standard `.ydk`)** : Le système gère nativement le format `.ydk` (utilisé par la majorité des simulateurs). Il permet d'importer une liste pour auditer sa viabilité (identifier les briques), et exporte systématiquement la "Decklist Ultime" générée par l'IA sous ce format pour des tests immédiats.
- **Taille de Deck Dynamique (Optimisation Pure)** : L'algorithme vise 40 cartes par défaut mais est autorisé à simuler et valider des tailles allant jusqu'à 60 cartes. S'il prouve mathématiquement qu'ajouter des cartes dilue le risque de piocher des Garnets inévitables tout en maintenant un taux d'ouverture de Starters supérieur à 85%, le système générera la liste étendue.
