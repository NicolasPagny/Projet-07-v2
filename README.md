# Introduction du projet

L'objectif du projet est de mettre en place un serveur API d'analyse de sentiment des tweets comprenant une intégration continue et un déploiement continu.

Les découpages des dossiers sont les suivants :

- répertoire parent contient : 
  - flask_app.py : le script flask qui permet de lancer l'API
  - preprocess_functions : contient les fonctions de prétraitements et du modèle de prédictions dont l'API utilise
  - requirements-tests.txt : indication des packages utilisés pour le test unitaire
  - requirements.txt : indication des packages utilisés pour l'API

- répertoire scripts contient 2 scripts bash que l'API utilise pour mettre à jour l'application et rédémarrer le serveur pour mettre en place la nouvelle version

- tests contient le test unitaire pour vérifier que le modèle produit bien des prédictions attendues

- .github/workflows contient le script .yml nécessaire pour la pipeline d'intégration continue et déploiement continu

# Détails d'installation sur le serveur cible
ces installations sont à faire manuellement

## Installation .venv
Le projet fonctionne avec un environnement virtuel .venv (bien respecter le nom de l'environnement virtuel) avec
python -m venv .venv

## ajouter les lignes ci-dessous en fin du fichier .venv/bin/activate :

## Ne pas modifier ces lignes
export FLASK_APP="flask_app"
export FLASK_RUN_PORT="5000"

## Utilisation avec Azure insights, copier la connection string
export APPLICATIONINSIGHTS_CONNECTION_STRING="xxx"

## token pour pouvoir effectuer le déploiement et le rédémérrage du serveur l'api token est également à renseigner dans "secrets" de github avec le nom "API_TOKEN_DEPLOY"
export API_TOKEN="XXX"