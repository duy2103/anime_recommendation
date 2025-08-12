"""
Anime Recommender System: Hybrid (Content-based, using Jikan API)
"""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.neighbors import NearestNeighbors
from src.data_loader import search_anime, get_anime_by_id, extract_features
import numpy as np

class AnimeRecommender:
    def __init__(self):
        self.tfidf = TfidfVectorizer(token_pattern=r"[a-zA-Z0-9-]+", stop_words='english')
        self.anime_df = None
        self.tfidf_matrix = None
        self.feature_matrix = None
        self.nn_model = None

    def build_content_model(self, anime_df):
        self.anime_df = anime_df.copy()
        self.tfidf_matrix = self.tfidf.fit_transform(self.anime_df['genres'])

    def recommend_by_title(self, liked_titles, top_n=10):
        # Search for each liked title and build a DataFrame
        dfs = [search_anime(title, limit=1) for title in liked_titles]
        liked_df = pd.concat(dfs, ignore_index=True)
        # Get more candidates by searching for similar genres
        all_genres = set(', '.join(liked_df['genres']).split(', '))
        candidates = []
        for genre in all_genres:
            if genre:
                candidates.append(search_anime(genre, limit=10))
        candidate_df = pd.concat(candidates, ignore_index=True).drop_duplicates('mal_id')
        self.build_content_model(candidate_df)
        # Find indices of liked anime in candidate_df
        indices = candidate_df[candidate_df['title'].isin(liked_df['title'])].index
        if len(indices) == 0:
            return []
        sim_scores = linear_kernel(self.tfidf_matrix[indices], self.tfidf_matrix).mean(axis=0)
        sim_scores = list(enumerate(sim_scores))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        recommended = [candidate_df.iloc[i]['title'] for i, score in sim_scores if candidate_df.iloc[i]['title'] not in liked_titles][:top_n]
        return recommended

    def build_feature_matrix(self, anime_df):
        # Extract features for each anime
        features = []
        for _, row in anime_df.iterrows():
            anime = get_anime_by_id(row['mal_id'])
            features.append(extract_features(anime))
        self.feature_matrix = np.array(features)
        self.anime_df = anime_df.reset_index(drop=True)
        self.nn_model = NearestNeighbors(n_neighbors=15, metric='euclidean')
        self.nn_model.fit(self.feature_matrix)

    def recommend_knn(self, liked_titles, top_n=10):
        # Search for each liked title and build a DataFrame
        dfs = [search_anime(title, limit=1) for title in liked_titles]
        liked_df = pd.concat(dfs, ignore_index=True)
        # Build candidate pool (union of genres from liked anime)
        all_genres = set(', '.join(liked_df['genres']).split(', '))
        candidates = []
        for genre in all_genres:
            if genre:
                candidates.append(search_anime(genre, limit=10))
        candidate_df = pd.concat(candidates, ignore_index=True).drop_duplicates('mal_id')
        self.build_feature_matrix(candidate_df)
        # Build user profile vector (mean of liked anime vectors)
        liked_features = []
        for _, row in liked_df.iterrows():
            anime = get_anime_by_id(row['mal_id'])
            liked_features.append(extract_features(anime))
        if not liked_features:
            return []
        user_vec = np.mean(liked_features, axis=0).reshape(1, -1)
        # Find nearest neighbors
        dists, indices = self.nn_model.kneighbors(user_vec, n_neighbors=top_n)
        recommended = [self.anime_df.iloc[i]['title'] for i in indices[0] if self.anime_df.iloc[i]['title'] not in liked_titles][:top_n]
        return recommended

    def recommend_by_genre(self, genres, top_n=10):
        # Search for anime by genre
        candidates = [search_anime(genre, limit=10) for genre in genres]
        candidate_df = pd.concat(candidates, ignore_index=True).drop_duplicates('mal_id')
        candidate_df = candidate_df.sort_values('score', ascending=False)
        return candidate_df['title'].head(top_n).tolist()

    def recommend_by_onboarding(self, genres, types, era, themes, tone, age, lang, top_n=10):
        # Build a search query from onboarding answers
        queries = list(genres) + list(types) + list(themes)
        # Era to year range
        era_map = {
            "1980s": (1980, 1989),
            "1990s": (1990, 1999),
            "2000s": (2000, 2009),
            "2010s": (2010, 2019),
            "2020s": (2020, 2025)
        }
        year_min, year_max = era_map.get(era, (1980, 2025))
        # Search for candidates
        candidates = []
        for q in queries:
            candidates.append(search_anime(q, limit=10))
        candidate_df = pd.concat(candidates, ignore_index=True).drop_duplicates('mal_id')
        # Filter by year if possible (using Jikan API for details)
        filtered = []
        for _, row in candidate_df.iterrows():
            anime = get_anime_by_id(row['mal_id'])
            year = 0
            if anime.get('aired', {}) and anime.get('aired', {}).get('from'):
                try:
                    year = int(anime['aired']['from'][:4])
                except:
                    year = 0
            if year_min <= year <= year_max:
                filtered.append(anime)
        if not filtered:
            filtered = [get_anime_by_id(row['mal_id']) for _, row in candidate_df.iterrows()]
        # Build feature matrix
        features = [extract_features(a) for a in filtered]
        self.feature_matrix = np.array(features)
        self.anime_df = pd.DataFrame(filtered)
        # Build user profile vector from answers
        # For MVP: genres, types, themes as multi-hot; era as normalized year; tone/age/lang ignored for now
        all_genres = [
            "Action", "Adventure", "Comedy", "Drama", "Fantasy", "Horror", "Mystery", "Romance", "Sci-Fi", "Slice of Life", "Sports", "Supernatural"
        ]
        genre_vec = [1 if g in genres else 0 for g in all_genres]
        all_types = ["TV", "Movie", "OVA", "ONA", "Special", "Music"]
        type_vec = [1 if t in types else 0 for t in all_types]
        # Era as normalized year (middle of range)
        year_norm = ((year_min + year_max) / 2 - 1980) / (2025 - 1980)
        # Score: neutral (0.5)
        score_norm = 0.5
        # Source: all zeros for now
        all_sources = ["Manga", "Original", "Light novel", "Visual novel", "Game", "Other"]
        source_vec = [0] * len(all_sources)
        user_vec = np.array(genre_vec + [score_norm, year_norm] + type_vec + source_vec).reshape(1, -1)
        # KNN
        if len(self.feature_matrix) == 0:
            return []
        nn_model = NearestNeighbors(n_neighbors=top_n, metric='euclidean')
        nn_model.fit(self.feature_matrix)
        dists, indices = nn_model.kneighbors(user_vec, n_neighbors=top_n)
        recs = [filtered[i] for i in indices[0]]
        # Add image_url for display (from Jikan API)
        for r in recs:
            if 'images' in r and 'jpg' in r['images']:
                r['image_url'] = r['images']['jpg'].get('large_image_url', '') or r['images']['jpg'].get('image_url', '')
            else:
                r['image_url'] = ''
        return recs
