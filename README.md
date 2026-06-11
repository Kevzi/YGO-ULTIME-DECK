# YGO ULTIME DECK

**YGO ULTIME DECK** est un moteur mathématique et analytique backend pour optimiser les decks Yu-Gi-Oh!. 
Il intègre une ingestion de données YGOJSON, du "Counter-Matching" sémantique, et une simulation hypergéométrique via Monte-Carlo pour construire des listes mathématiquement supérieures.

## Fonctionnalités

- **Ingestion YGOJSON** : Téléchargement et mise en cache des données officielles (format v0.6.0).
- **Auto-Tagging Sémantique** : Parseur de textes de cartes (Regex PSCT) permettant de déterminer les rôles (Starters, Extenders).
- **Simulateur de Combos** : Moteur de probabilités utilisant Monte-Carlo (jusqu'à 100 000 itérations) supportant la pioche dynamique.
- **Intelligence Counter-Matching** : Simulation de résilience face aux interruptions courantes de la méta.
- **Générateur YDK** : Optimiseur de taille de deck (40 à 60 cartes) et exportation vers les simulateurs (Edopro, Omega).

## Installation (Développement)

Ce projet utilise [uv](https://docs.astral.sh/uv/) pour une gestion ultrarapide des dépendances et de l'environnement virtuel.

1. Installer `uv` si ce n'est pas déjà fait.
2. Synchroniser les dépendances :
   ```bash
   uv sync
   ```

## Utilisation

L'outil offre une interface en ligne de commande (CLI) propulsée par Typer et formatée avec Rich.

Pour voir l'aide globale :
```bash
uv run ygo-deck --help
```

*(Des commandes supplémentaires comme `--update` seront ajoutées lors des prochains sprints).*

## Dépendances clés
- Python 3.12+
- `typer` (CLI)
- `pydantic` v2 (Modèles de données strictes)
- `rich` (Formatage terminal)
- `pytest`, `ruff` (Tests et Qualité)
