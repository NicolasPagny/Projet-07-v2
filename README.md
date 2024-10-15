# Projet-07-v2

Le projet fonctionne avec un environnement virtuel .venv (bien respecter le nom de l'environnement virtuel) avec
python -m venv .venv

ajouter les lignes ci-dessous en fin du fichier .venv/bin/activate :

# Ne pas modifier ces lignes
export FLASK_APP="flask_app"
export FLASK_RUN_PORT="5000"

# Utilisation avec Azure insights, copier la connection string
export APPLICATIONINSIGHTS_CONNECTION_STRING="xxx"

# token pour pouvoir effectuer le déploiement et le rédémérrage du serveur
# l'api token est également à renseigner dans "secrets" de github avec le nom "API_TOKEN_DEPLOY"
export API_TOKEN="XXX"