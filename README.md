# 🎬 MovieFlix - Site de Streaming de Films

Un site web complet et fonctionnel pour découvrir et regarder des films en streaming, alimenté par TMDB et Vidcore.

## 🌟 Fonctionnalités

✅ **Barre de recherche** - Recherchez n'importe quel film en temps réel  
✅ **Section Tendances** - Les films les plus populaires cette semaine  
✅ **Catégories** - Action, Aventure, et bien d'autres  
✅ **Films les plus visionnés** - Découvrez les meilleurs films  
✅ **Lecteur vidéo Vidcore** - Streaming de qualité 4K sans pub  
✅ **Design moderne et réactif** - Fonctionne sur tous les appareils  

## 🛠️ Technologies utilisées

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3
- **API Films**: TMDB (The Movie Database)
- **Streaming**: Vidcore
- **Requêtes HTTP**: Python Requests

## 📋 Prérequis

- Python 3.7+
- pip (gestionnaire de paquets Python)
- Connexion internet

## 🚀 Installation

### 1. Clonez ou téléchargez le projet

```bash
cd movieflix
```

### 2. Créez un environnement virtuel (optionnel mais recommandé)

```bash
# Sur Windows
python -m venv venv
venv\Scripts\activate

# Sur macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Installez les dépendances

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

La clé API TMDB est déjà configurée dans `app.py`:
```python
TMDB_API_KEY = "8cbdc48d9bf8bef63fe12c023aaebf08"
```

## 🎯 Lancer le serveur

```bash
python app.py
```

Le serveur démarrera sur `http://localhost:5000`

Ouvrez votre navigateur et accédez à:
```
http://localhost:5000
```

## 📁 Structure du projet

```
movieflix/
├── app.py                 # Backend Flask
├── requirements.txt       # Dépendances Python
├── README.md             # Ce fichier
├── templates/
│   ├── index.html        # Page d'accueil
│   └── watch.html        # Page de lecture
└── static/
    └── style.css         # Styles CSS
```

## 🎬 Utilisation

### Page d'accueil
- Voir les films en tendance
- Parcourir les catégories (Action, Aventure, etc.)
- Utiliser la barre de recherche pour trouver un film

### Regarder un film
1. Cliquez sur "Regarder" sur n'importe quel film
2. Le lecteur Vidcore se chargera automatiquement
3. Profitez de votre film en 4K sans pub!

## 🔍 Fonctionnalités en détail

### Barre de recherche
- Tapez le titre d'un film
- Les résultats s'affichent automatiquement
- Cliquez sur un résultat pour regarder

### Tendances
- Met à jour chaque semaine
- Affiche les 12 films les plus populaires
- Inclus la note IMDB

### Catégories
- Action
- Aventure
- Et bien d'autres genres disponibles

### Lecteur Vidcore
- Qualité jusqu'à 4K
- Sans publicités
- Sous-titres en 30+ langues
- Compatible mobile

## 🐛 Dépannage

### Les films ne s'affichent pas
- Vérifiez votre connexion internet
- Assurez-vous que l'API TMDB est accessible
- Redémarrez le serveur Flask

### Le lecteur vidéo ne fonctionne pas
- Assurez-vous que Vidcore est accessible (vidcore.org)
- Vérifiez les paramètres de votre pare-feu
- Attendez quelques secondes avant de cliquer sur Regarder

### Port 5000 déjà utilisé
```bash
# Utilisez un port différent
python -c "from app import app; app.run(port=8000)"
```

## 📝 Notes importantes

⚠️ **API Keys**: Ne partagez JAMAIS votre clé API TMDB publiquement  
⚠️ **Streaming légal**: Vidcore fournit du contenu légal via des sources autorisées  
✅ **Gratuit**: Aucun frais, aucun abonnement requis  

## 🚀 Améliorations futures

- [ ] Système de favoris
- [ ] Historique de visionnage
- [ ] Critiques utilisateurs
- [ ] Listes de lecture personnalisées
- [ ] Mode sombre/clair
- [ ] Support des séries TV

## 📄 Licence

Projet à usage personnel et éducatif.

## 👨‍💻 Auteur

MovieFlix - Créé avec ❤️ pour les amateurs de films

## 📞 Support

Pour des problèmes ou des questions:
1. Vérifiez les prérequis
2. Consultez le dépannage
3. Redémarrez le serveur

---

**Bon streaming! 🎬🍿**
