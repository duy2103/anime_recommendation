"""
Data loader module for fetching anime data from MyAnimeList API (via Jikan).
"""
import requests
import pandas as pd

def search_anime(query, limit=10):
    """
    Search for anime by title using Jikan API.
    Returns a DataFrame of search results.
    """
    url = f"https://api.jikan.moe/v4/anime?q={query}&limit={limit}"
    response = requests.get(url)
    results = response.json().get('data', [])
    anime_list = []
    for anime in results:
        anime_list.append({
            'mal_id': anime['mal_id'],
            'title': anime['title'],
            'genres': anime.get('genres', []),  # keep as list of dicts
            'genres_str': ', '.join([g['name'] for g in anime.get('genres', [])]),
            'synopsis': anime.get('synopsis', ''),
            'score': anime.get('score', 0),
            'url': anime.get('url', ''),
            'images': anime.get('images', {}),
        })
    return pd.DataFrame(anime_list)

def get_anime_by_id(mal_id):
    """
    Fetch anime details by MAL ID using Jikan API.
    """
    url = f"https://api.jikan.moe/v4/anime/{mal_id}"
    response = requests.get(url)
    anime = response.json().get('data', {})
    return {
        'mal_id': anime.get('mal_id'),
        'title': anime.get('title'),
        'genres': anime.get('genres', []),  # keep as list of dicts
        'genres_str': ', '.join([g['name'] for g in anime.get('genres', [])]),
        'synopsis': anime.get('synopsis', ''),
        'score': anime.get('score', 0),
        'url': anime.get('url', ''),
        'images': anime.get('images', {}),
        'aired': anime.get('aired', {}),
        'type': anime.get('type', ''),
        'source': anime.get('source', ''),
    }

def extract_features(anime):
    """
    Given a Jikan anime dict, extract a feature vector.
    Features: genres (multi-hot), score (normalized), year (normalized), type (one-hot), source (one-hot)
    """
    # Genre encoding
    all_genres = [
        "Action", "Adventure", "Comedy", "Drama", "Fantasy", "Horror", "Mystery", "Romance", "Sci-Fi", "Slice of Life", "Sports", "Supernatural"
    ]
    # genres is now a list of dicts
    genre_set = set([g['name'] for g in anime.get('genres', [])])
    genre_vec = [1 if g in genre_set else 0 for g in all_genres]
    # Score (normalize 0-10)
    score = anime.get('score', 0) or 0
    score_norm = score / 10.0
    # Year (normalize 1980-2025)
    year = 0
    if anime.get('aired', {}).get('from'):
        try:
            year = int(anime['aired']['from'][:4])
        except:
            year = 0
    year_norm = (year - 1980) / (2025 - 1980) if 1980 <= year <= 2025 else 0
    # Type one-hot
    all_types = ["TV", "Movie", "OVA", "ONA", "Special", "Music"]
    type_vec = [1 if anime.get('type') == t else 0 for t in all_types]
    # Source one-hot
    all_sources = ["Manga", "Original", "Light novel", "Visual novel", "Game", "Other"]
    source_vec = [1 if anime.get('source') == s else 0 for s in all_sources]
    # Combine all features
    return genre_vec + [score_norm, year_norm] + type_vec + source_vec
