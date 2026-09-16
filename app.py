from flask import Flask, render_template, request, jsonify
import requests
from functools import lru_cache

app = Flask(__name__)

# Configuration TMDB
TMDB_API_KEY = "8cbdc48d9bf8bef63fe12c023aaebf08"
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

# Configuration Vidcore
VIDCORE_BASE = "https://vidcore.org/embed/movie"

@lru_cache(maxsize=100)
def get_trending_movies():
    """Récupère les films en tendance"""
    try:
        url = f"{TMDB_BASE_URL}/trending/movie/week"
        params = {"api_key": TMDB_API_KEY}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("results", [])
    except Exception as e:
        print(f"Erreur tendances: {e}")
        return []

@lru_cache(maxsize=100)
def get_movies_by_category(genre_id):
    """Récupère les films par catégorie"""
    try:
        url = f"{TMDB_BASE_URL}/discover/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "with_genres": genre_id,
            "sort_by": "popularity.desc",
            "page": 1
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("results", [])
    except Exception as e:
        print(f"Erreur catégorie: {e}")
        return []

def get_genres():
    """Récupère la liste des genres"""
    try:
        url = f"{TMDB_BASE_URL}/genre/movie/list"
        params = {"api_key": TMDB_API_KEY}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("genres", [])
    except Exception as e:
        print(f"Erreur genres: {e}")
        return []

def search_movies(query):
    """
    Recherche des films via l'API TMDB.
    ⚠️ SÉCURITÉ: Cette fonction ne révèle JAMAIS la clé API au client.
    La clé API est utilisée côté serveur UNIQUEMENT.
    """
    try:
        # Validation: nettoyer et limiter la requête
        if not query or not isinstance(query, str):
            return []
        
        query = query.strip()
        if len(query) < 2 or len(query) > 100:
            return []
        
        # ⚠️ SÉCURITÉ: L'appel API se fait côté serveur UNIQUEMENT
        # Le client ne voit JAMAIS la clé API
        url = f"{TMDB_BASE_URL}/search/movie"
        params = {
            "api_key": TMDB_API_KEY,  # ← Restera côté serveur
            "query": query,
            "page": 1
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json().get("results", [])
    except Exception as e:
        # ⚠️ SÉCURITÉ: Ne pas révéler les détails d'erreur au client
        print(f"Erreur recherche (serveur): {e}")
        return []

def format_movies(movies):
    """Formate les films pour le frontend"""
    formatted = []
    for movie in movies[:12]:  # Limite à 12 films
        formatted.append({
            "id": movie.get("id"),
            "title": movie.get("title", "Titre inconnu"),
            "poster_path": TMDB_IMAGE_BASE + movie.get("poster_path", "") if movie.get("poster_path") else "",
            "overview": movie.get("overview", ""),
            "rating": movie.get("vote_average", 0),
            "release_date": movie.get("release_date", "")
        })
    return formatted

@app.route("/")
def index():
    """Page d'accueil"""
    trending = format_movies(get_trending_movies())
    genres = get_genres()
    
    # Récupère les catégories principaux
    action_movies = format_movies(get_movies_by_category(28))  # Action
    adventure_movies = format_movies(get_movies_by_category(12))  # Adventure
    
    return render_template("index.html", 
                         trending=trending,
                         action_movies=action_movies,
                         adventure_movies=adventure_movies,
                         genres=genres)

@app.route("/search")
def search():
    """
    Endpoint de recherche.
    ⚠️ SÉCURITÉ: Le client envoie juste la requête de recherche.
    Toutes les appels API se font côté serveur avec la clé API.
    Le client reçoit UNIQUEMENT les données formatées.
    """
    try:
        # Récupère et valide la requête depuis le client
        query = request.args.get("q", "").strip()
        
        # Validation: vérifier que la requête est valide
        if not query or len(query) < 2:
            return jsonify({"results": [], "error": None})
        
        # ⚠️ SÉCURITÉ: Traitement côté serveur UNIQUEMENT
        # La clé API ne voyage JAMAIS vers le client
        movies = search_movies(query)
        
        # Retourne UNIQUEMENT les données formatées
        return jsonify({"results": format_movies(movies), "error": None})
    
    except Exception as e:
        # ⚠️ SÉCURITÉ: Ne pas révéler les erreurs au client
        print(f"Erreur endpoint search: {e}")
        return jsonify({"results": [], "error": None})

@app.route("/category/<int:genre_id>")
def category(genre_id):
    """Page de catégorie"""
    movies = format_movies(get_movies_by_category(genre_id))
    genres = get_genres()
    return render_template("category.html", 
                         movies=movies,
                         genres=genres,
                         genre_id=genre_id)

@app.route("/watch/<int:movie_id>")
def watch(movie_id):
    """
    Page de lecture d'un film avec infos complètes.
    ⚠️ SÉCURITÉ: Toutes les appels API se font côté serveur.
    L'URL Bitcore est générée côté serveur et envoyée au client.
    Le client ne voit JAMAIS la clé API.
    """
    print("movie ID " + str(movie_id))
    try:
        # Validation: vérifier que l'ID du film est valide
        if not movie_id or movie_id < 1:
            raise ValueError("ID du film invalide")
        
        # ⚠️ SÉCURITÉ: Appel API côté serveur UNIQUEMENT
        # La clé API ne voyage JAMAIS vers le client
        url = f"{TMDB_BASE_URL}/movie/{movie_id}"
        params = {"api_key": TMDB_API_KEY}  # ← Reste côté serveur
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        movie_data = response.json()
        
        movie_info = {
            "id": movie_id,
            "title": movie_data.get("title", "Titre inconnu"),
            "overview": movie_data.get("overview", "Aucune description disponible"),
            "poster_path": TMDB_IMAGE_BASE + movie_data.get("poster_path", "") if movie_data.get("poster_path") else "",
            "backdrop_path": TMDB_IMAGE_BASE + movie_data.get("backdrop_path", "") if movie_data.get("backdrop_path") else "",
            "rating": movie_data.get("vote_average", 0),
            "release_date": movie_data.get("release_date", ""),
            "runtime": movie_data.get("runtime", 0),
            "genres": [g.get("name") for g in movie_data.get("genres", [])],
            "budget": movie_data.get("budget", 0),
            "revenue": movie_data.get("revenue", 0)
        }
        
        # ⚠️ SÉCURITÉ: L'URL Bitcore est générée côté serveur
        # Le client reçoit UNIQUEMENT l'URL du lecteur, pas la clé API
        bitcore_url = f"{VIDCORE_BASE}/{movie_id}"
        return render_template("watch.html", 
                             movie=movie_info, 
                             movie_id=movie_id,
                             bitcore_url=bitcore_url)
    except Exception as e:
        # ⚠️ SÉCURITÉ: Ne pas révéler les erreurs détaillées au client
        print(f"Erreur lors de la récupération du film (serveur): {e}")
        return render_template("watch.html", 
                             movie={"id": movie_id, "title": "Film non disponible"},
                             movie_id=movie_id,
                             bitcore_url=f"{VIDCORE_BASE}/{movie_id}")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
