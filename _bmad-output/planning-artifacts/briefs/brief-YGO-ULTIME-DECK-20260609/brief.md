---
title: YGO ULTIME DECK - Product Brief
status: draft
created: 2026-06-09
updated: 2026-06-09
---

# YGO ULTIME DECK - Product Brief

## 1. Vision & Objectif Global
Créer un algorithme d'optimisation de deck Yu-Gi-Oh! "Anti-Méta", piloté par l'analyse sémantique et les mathématiques.
L'objectif est d'éliminer la part de hasard liée à la construction de deck et d'offrir un "avantage déloyal" (mais légal) en tournoi compétitif, avec à long terme une ambition de commercialisation et de monétisation (ex: Patreon, modèle freemium) sous la forme d'une application Web aboutie.

## 2. Le Problème
Actuellement, la majorité des joueurs construisent leurs decks de manière intuitive ou en copiant aveuglément des listes. Cela entraîne un manque de consistance chronique (mains mortes ou "briques") et une mauvaise adaptation stratégique face aux decks dominants (méta ultra-rapide). De plus, face à un métajeu complexe, le calcul mental précis des probabilités complexes d'ouverture (trouver l'équilibre parfait entre Starters, Extenders et Hand Traps) dépasse les capacités humaines.

## 3. La Solution
Un produit (initialement un moteur backend en Python) agissant comme une "machine à construire le deck parfait" :
- **Identification des Choke Points** : Analyse sémantique des faiblesses des meilleurs decks du moment.
- **Counter-Matching (Le Moat / L'Avantage Compétitif)** : Contrairement aux calculateurs existants qui se contentent d'évaluer une liste donnée, notre moteur génère activement la liste en sélectionnant automatiquement un archétype immunisé aux menaces actuelles.
- **Optimisation Mathématique** : Utilisation de la distribution hypergéométrique multivariée (avec algorithme anti-overflow) pour calculer au pourcentage près le ratio parfait des cartes.
## 4. Public Cible & Stratégie de Déploiement
- **V1 (Phase Bêta Fermée)** : Le script Python en ligne de commande sera utilisé exclusivement par le créateur et un cercle très restreint de "bêta-testeurs" compétitifs. Cette approche garantit d'obtenir des retours terrain sur la viabilité réelle des listes sans fuiter l'algorithme "Counter-Matching".
- **V2 (Phase Commerciale)** : Application Web avec interface graphique simple, destinée à la communauté élargie de joueurs compétitifs prêts à payer pour un calculateur de probabilités avancé (via Patreon ou accès premium).

## 5. Métriques de Succès (V1)
- **Succès Technique (Immédiat)** : Capacité de l'algorithme à ingérer YGOJSON et à calculer des combinaisons hypergéométriques sans saturer la mémoire (crash ou overflow) via un algorithme logarithmique.
- **Succès Compétitif (Validation Terrain)** : L'outil doit générer des decks permettant de maintenir un taux d'ouverture de "Starters" d'au moins 85 % lors des parties réelles, menant à une domination mesurable en tournoi local (OTS) contre les decks de la méta actuelle (ex: Kewl Tune, Branded Dracotail, DoomZ).

## 6. Risques & Dépendances Critiques
Le talon d'Achille du projet est la dépendance à **YGOJSON**, un dépôt open-source dont les changements de schéma ou l'abandon bloqueraient l'outil.
- **Plan d'Atténuation A (Immédiat)** : Mise en place d'un système de caching local automatisé (téléchargement quotidien de `aggregate.zip`) pour figer la base de données de la méta connue en cas de panne.
- **Plan d'Atténuation B (Le "Scraper" de secours)** : Développement d'un scraper Python léger en tâche de fond, capable d'extraire directement les textes des cartes depuis l'API de YGOPRODECK ou les pages Yugipedia en cas de défaillance définitive de YGOJSON.

## 7. Expérience Utilisateur (UI/UX) de la V2
- **La Magie en un Clic** : Contrairement aux calculateurs manuels, l'utilisateur indique l'objectif ("Battre le Top 3") et son style de jeu (ex: "Bannissement"). L'outil sélectionne le moteur optimal (ex: Kashtira) et génère instantanément la "Decklist Ultime" de 40 cartes, accompagnée de ses statistiques (ex: 85% de Starters).
- **Personnalisation Intelligente** : L'utilisateur peut "verrouiller" des cartes physiques qu'il possède déjà ; l'algorithme recalcule et réajuste dynamiquement le reste du deck autour de ces contraintes pour conserver une consistance parfaite.

## 8. Modèle de Monétisation (Freemium Stratégique)
- **Le Produit d'Appel (Gratuit)** : Un calculateur hypergéométrique de pointe et simulateur de mains ultra-fluide. Il sert d'aimant à trafic massif pour dominer le SEO et écraser la concurrence gratuite sur les réseaux.
- **L'Offre Premium (Abonnement / Patreon)** : Accès exclusif à "L'Intelligence Stratégique". Derrière le mur payant se trouvent le bouton de génération du deck Anti-Méta, la base de données des "Choke Points", l'algorithme d'auto-tagging, et l'accès aux listes optimales avant les grands événements (YCS). On attire avec la calculatrice, on vend l'intelligence.
