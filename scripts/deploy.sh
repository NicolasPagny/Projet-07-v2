#!/bin/bash

# Récupérer les dernières modifications de la branche main
echo "Mise à jour du dépôt Git..."
if git pull origin main --no-rebase; then
    echo "Mise à jour réussie."
else
    echo "Echec de la mise à jour depuis GitHub. Déploiement annulé."
    exit 1
fi