#!/bin/bash

echo "🎬 MovieFlix - Démarrage du serveur..."
echo ""

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 n'est pas installé"
    exit 1
fi

# Installer les dépendances si nécessaire
if ! python3 -c "import flask" 2>/dev/null
then
    echo "📦 Installation des dépendances..."
    pip install -r requirements.txt
fi

echo "✅ Démarrage du serveur Flask..."
echo ""
echo "🌍 Ouvrez votre navigateur à: http://localhost:5000"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter le serveur"
echo ""

python3 app.py
