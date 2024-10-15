#!/bin/bash

# Tuer tous les processus gunicorn
echo "Arrêt de Gunicorn..."
pkill -f gunicorn

#Sleep
sleep 5
 
#Go in the good directory
cd /home/nicolaspagny/projet07v4

# Activer l'environnement virtuel
echo "Activation de l'environnement virtuel..."
source .venv/bin/activate

# Installer les dépendances
echo "Installation des dépendances..."
pip install -r requirements.txt

# Démarrer Gunicorn
echo "Démarrage de Gunicorn..."
gunicorn -b 0.0.0.0:5000 flask_app:app > output.log 2> errors.log &

# Désactiver l'environnement virtuel
deactivate

# Vérifier que Gunicorn a bien démarré
if pgrep gunicorn > /dev/null; then
    echo "Gunicorn a redémarré avec succès."
else
    echo "Erreur : Gunicorn n'a pas redémarré."
    exit 1
fi
