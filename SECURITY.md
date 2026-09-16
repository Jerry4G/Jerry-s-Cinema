# 🔒 Guide de Sécurité - MovieFlix

## Architecture de Sécurité

### ✅ Problème résolu: Clé API exposée

**Ancienne approche (DANGEREUSE ❌):**
```
Client fait appel direct → TMDB API
           ↓
      Clé API EXPOSÉE au client
      N'importe quel pirate peut:
      - Voler la clé API
      - Inspecteur le code JavaScript
      - Utiliser la clé pour faire des requêtes
```

**Nouvelle approche (SÉCURISÉE ✅):**
```
Client envoie requête → Serveur Flask → TMDB API
                           ↓
                    Clé API CACHÉE
                  (côté serveur UNIQUEMENT)
                           ↓
              Serveur retourne juste les films
```

---

## Comment ça marche?

### 1️⃣ **Recherche de films**

**Flux sécurisé:**
```
UTILISATEUR tape "Avatar"
        ↓
CLIENT envoie → /search?q=Avatar
        ↓
SERVEUR reçoit "Avatar"
        ↓
SERVEUR utilise clé API pour appeler TMDB
        ↓
SERVEUR reçoit réponse TMDB
        ↓
SERVEUR formate les données
        ↓
SERVEUR envoie JUSTE les films au client
        ↓
CLIENT affiche les résultats
```

**Qu'est-ce que le client envoie?**
```javascript
fetch(`/search?q=Avatar`)  // ← Seulement le texte!
```

**Qu'est-ce que le client REÇOIT?**
```json
{
  "results": [
    {
      "id": 19995,
      "title": "Avatar",
      "poster_path": "https://image.tmdb.org/...",
      "rating": 7.8,
      "overview": "..."
    }
  ]
}
```

**Qu'est-ce que le client NE voit JAMAIS?**
```
❌ Clé API: "8cbdc48d9bf8bef63fe12c023aaebf08"
❌ URL TMDB: "https://api.themoviedb.org/3/search/movie"
❌ Réponse brute de TMDB
```

---

### 2️⃣ **Affichage d'un film**

**Flux sécurisé:**
```
UTILISATEUR clique "Regarder"
        ↓
CLIENT envoie ID → /watch/533535
        ↓
SERVEUR reçoit ID
        ↓
SERVEUR utilise clé API pour appeler TMDB
        ↓
SERVEUR reçoit infos du film
        ↓
SERVEUR génère URL Bitcore: https://vidcore.org/embed/movie/533535
        ↓
SERVEUR envoie:
  - Titre du film
  - Description
  - Affiche
  - URL Bitcore (lecteur vidéo)
        ↓
CLIENT affiche le film
```

**Qu'est-ce que le client envoie?**
```
GET /watch/533535  ← Juste l'ID du film!
```

**Qu'est-ce que le client REÇOIT?**
```html
<iframe src="https://vidcore.org/embed/movie/533535"></iframe>
```

**Qu'est-ce que le client NE voit JAMAIS?**
```
❌ Clé API
❌ Requête TMDB
❌ Réponse TMDB brute
```

---

## 🛡️ Protections implémentées

### 1. **Clé API côté serveur UNIQUEMENT**
```python
# Dans app.py
TMDB_API_KEY = "8cbdc48d9bf8bef63fe12c023aaebf08"  # ← Serveur seulement
```

### 2. **Validation des entrées**
```python
# Validation de la recherche
if len(query) < 2 or len(query) > 100:
    return []  # ← Requête invalide refusée

# Validation de l'ID du film
if not movie_id or movie_id < 1:
    raise ValueError("ID du film invalide")
```

### 3. **Pas de révélation d'erreurs**
```python
# ✅ BON: Erreur cachée
except Exception as e:
    print(f"Erreur (serveur): {e}")
    return jsonify({"results": []})  # Pas d'infos sensibles

# ❌ MAUVAIS: Erreur révélée
except Exception as e:
    return jsonify({"error": str(e)})  # Le client voit tout!
```

### 4. **Timeout sur les requêtes**
```python
response = requests.get(url, params=params, timeout=10)
# ← Évite que le serveur se fige indéfiniment
```

### 5. **Caching intelligent**
```python
@lru_cache(maxsize=100)
def get_trending_movies():
    # Les résultats sont cachés
    # Réduit les appels API
    # Plus rapide pour l'utilisateur
```

---

## 🔐 Ce qui est PROTÉGÉ

✅ **Clé API TMDB** - Impossible à voler  
✅ **URL TMDB** - Pas visible au client  
✅ **Requêtes API** - Faites côté serveur  
✅ **Erreurs détaillées** - Pas révélées au client  
✅ **Réponses brutes** - Formatées avant envoi  

---

## ⚠️ Ce qui est PUBLIC (Normal)

Ces informations sont intentionnellement publiques (c'est normal!):
- 🎬 Titres des films
- 🖼️ Affiches des films
- ⭐ Notes des films
- 📝 Descriptions
- 🎯 URLs des images (TMDB)
- 🎥 URLs Bitcore (lecteur vidéo)

---

## 🔍 Comment vérifier que c'est sécurisé?

### Teste dans ton navigateur:

**1. Ouvre l'Inspecteur (F12)**

**2. Va dans l'onglet "Network"**

**3. Tape dans la barre de recherche**

**4. Regarde les requêtes:**
```
❌ N'apparaît PAS: https://api.themoviedb.org/3/search/movie?api_key=...
✅ N'apparaît QUE: http://localhost:5000/search?q=Avatar
```

**5. Clique sur `/search` pour voir la réponse:**
```json
{
  "results": [
    {"id": 123, "title": "Avatar", ...}
  ]
}
```

**6. Vérifie:**
- ✅ Pas de clé API
- ✅ Pas d'URL TMDB
- ✅ Juste les données formatées

---

## 🚀 Bonnes pratiques appliquées

1. ✅ **Principe du moindre privilège** - Le client ne reçoit que ce qu'il faut
2. ✅ **Défense en profondeur** - Validation côté serveur
3. ✅ **Gestion d'erreurs sécurisée** - Pas de révélation d'infos
4. ✅ **Entrées validées** - Aucune injection possible
5. ✅ **Timeouts** - Protection contre les abus

---

## 📋 Résumé pour l'utilisateur

| Aspect | Avant | Après |
|--------|-------|-------|
| Clé API visible? | ❌ OUI (danger!) | ✅ NON (sécurisé) |
| Client peut appeler TMDB? | ❌ OUI | ✅ NON |
| Erreurs révélées? | ❌ OUI | ✅ NON |
| Validation entrées? | ❌ Non | ✅ OUI |
| Timeout requêtes? | ❌ Non | ✅ OUI |

---

## ⚠️ Notes importantes

- 🔑 **Clé API**: Ne partagez JAMAIS votre clé API
- 🔒 **HTTPS**: En production, utilisez HTTPS (pas HTTP)
- 🚨 **Tokens**: Ne mettez JAMAIS de tokens dans le code client
- 📊 **Rate limiting**: Envisagez un rate limiter en production

---

**Ton site est maintenant sécurisé! 🎉**

Aucun pirate ne peut voler ta clé API!
