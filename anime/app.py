"""
Streamlit app for Anime Recommender System using MyAnimeList API (Jikan)
"""
import os
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['VECLIB_MAXIMUM_THREADS'] = '1'
os.environ['NUMEXPR_NUM_THREADS'] = '1'

import streamlit as st
from src.recommender import AnimeRecommender
import joblib
import pandas as pd
import time
import numpy as np
from src.config import GENRES, TYPES, THEMES, TONES, AGE_RATINGS, LANG_PREF

st.title("Anime Recommender System (MAL API)")

# Session state for user lists
if 'to_watch' not in st.session_state:
    st.session_state['to_watch'] = []
if 'watched' not in st.session_state:
    st.session_state['watched'] = []
if 'not_interested' not in st.session_state:
    st.session_state['not_interested'] = []

recommender = AnimeRecommender()

user_type = st.radio("Are you new to anime or a returning watcher?", ["New to anime", "Returning user"])

if user_type == "New to anime":
    st.header("Let's get to know your taste!")
    genres = GENRES
    types = TYPES
    # Only use factors that match the ML features
    selected_genres = st.multiselect("Pick your favorite genres:", genres)
    selected_types = st.multiselect("Preferred anime type(s):", types)
    episodes = st.number_input("Preferred number of episodes (0 for any):", min_value=0, max_value=1000, value=0)
    year = st.number_input("Preferred year (0 for any):", min_value=0, max_value=2025, value=0)
    duration_min = st.number_input("Preferred duration per episode (minutes, 0 for any):", min_value=0, max_value=200, value=0)
    if st.button("Get ML Recommendations!"):
        with st.spinner('Finding recommendations...'):
            # Build user vector
            features_df = pd.read_csv('data/mal_anime_features.csv')
            # Get feature columns as in model training
            ignore_cols = ['mal_id', 'score']
            feature_cols = [c for c in features_df.columns if c not in ignore_cols and features_df[c].dtype in [np.int64, np.float64, np.int32, np.float32]]
            # Build user_vec as a dict for all feature_cols
            user_vec_dict = {col: 0 for col in feature_cols}
            # Fill genre columns
            for col in feature_cols:
                if col.startswith('genre_'):
                    genre = col.replace('genre_', '')
                    user_vec_dict[col] = 1 if genre in selected_genres else 0
            # Fill type columns
            for col in feature_cols:
                if col.startswith('type_'):
                    t = col.replace('type_', '')
                    user_vec_dict[col] = 1 if t in selected_types else 0
            # Fill numeric fields
            if 'episodes' in feature_cols:
                user_vec_dict['episodes'] = episodes
            if 'year' in feature_cols:
                user_vec_dict['year'] = year
            if 'duration_min' in feature_cols:
                user_vec_dict['duration_min'] = duration_min
            # Build DataFrame
            user_vec_df = pd.DataFrame([user_vec_dict])
            scaler = joblib.load('data/knn_scaler.joblib')
            knn = joblib.load('data/knn_model.joblib')
            user_vec_scaled = scaler.transform(user_vec_df)
            dists, indices = knn.kneighbors(user_vec_scaled, n_neighbors=6)
            clean_df = pd.read_csv('data/mal_anime_clean.csv').set_index('mal_id')
            st.subheader('Top Recommendations:')
            for i, rec_idx in enumerate(indices[0][1:]):
                rec_id = features_df.iloc[rec_idx]['mal_id']
                rec = clean_df.loc[rec_id]
                st.markdown(f"**{i+1}. {rec['title']}**  ")
                st.write(f"Genres: {rec['genres']}")
                st.write(f"Score: {rec['score']}")
                st.write(rec['synopsis'])
                if pd.notna(rec['image_url']) and rec['image_url']:
                    st.image(rec['image_url'], width=200)
                st.markdown('---')

elif user_type == "Returning user":
    st.header("How would you like to get recommendations?")
    mode = st.radio("Choose a mode:", ["Based on anime I've watched", "Explore new options"])
    liked_list = []
    if mode == "Based on anime I've watched":
        liked = st.text_area("Enter anime titles you've enjoyed (comma separated):")
        liked_list = [x.strip() for x in liked.split(',') if x.strip()]
        if st.button("Get ML Recommendations!") and liked_list:
            with st.spinner('Finding recommendations...'):
                features_df = pd.read_csv('data/mal_anime_features.csv')
                clean_df = pd.read_csv('data/mal_anime_clean.csv').set_index('mal_id')
                scaler = joblib.load('data/knn_scaler.joblib')
                knn = joblib.load('data/knn_model.joblib')
                # Get feature vectors for liked anime
                liked_ids = []
                for title in liked_list:
                    try:
                        liked_ids.append(int(clean_df[clean_df['title'] == title].index[0]))
                    except:
                        pass
                liked_vecs = features_df[features_df['mal_id'].isin(liked_ids)].drop(columns=['mal_id','score']).values
                if len(liked_vecs) == 0:
                    st.warning("No matching anime found in dataset.")
                else:
                    user_vec = liked_vecs.mean(axis=0).reshape(1, -1)
                    user_vec_scaled = scaler.transform(user_vec)
                    dists, indices = knn.kneighbors(user_vec_scaled, n_neighbors=6)
                    st.subheader('Top Recommendations:')
                    for i, rec_idx in enumerate(indices[0][1:]):
                        rec_id = features_df.iloc[rec_idx]['mal_id']
                        rec = clean_df.loc[rec_id]
                        st.markdown(f"**{i+1}. {rec['title']}**  ")
                        st.write(f"Genres: {rec['genres']}")
                        st.write(f"Score: {rec['score']}")
                        st.write(rec['synopsis'])
                        if pd.notna(rec['image_url']) and rec['image_url']:
                            st.image(rec['image_url'], width=200)
                        st.markdown('---')
    elif mode == "Explore new options":
        genres = GENRES
        types = TYPES
        eras = ["1980s", "1990s", "2000s", "2010s", "2020s"]
        themes = THEMES
        tones = TONES
        age_ratings = AGE_RATINGS
        lang_pref = LANG_PREF
        selected_genres = st.multiselect("Pick your favorite genres:", genres)
        selected_types = st.multiselect("Preferred anime type(s):", types)
        selected_era = st.selectbox("Preferred release era:", eras)
        selected_themes = st.multiselect("Preferred themes:", themes)
        selected_tone = st.selectbox("Story tone:", tones)
        selected_age = st.selectbox("Age rating:", age_ratings)
        selected_lang = st.selectbox("Language preference:", lang_pref)
    if st.button("Get Recommendations!"):
        if mode == "Based on anime I've watched" and liked_list:
            recs = recommender.recommend_knn(liked_list)
        else:
            recs = recommender.recommend_by_onboarding(selected_genres, selected_types, selected_era, selected_themes, selected_tone, selected_age, selected_lang)
        st.session_state['recommendations'] = recs
        st.session_state['rec_index'] = 0

# Tinder-style swipe interface
if 'recommendations' in st.session_state and st.session_state['recommendations']:
    recs = st.session_state['recommendations']
    idx = st.session_state.get('rec_index', 0)
    # User feedback loop: allow users to rate recommendations
    if 'feedback' not in st.session_state:
        st.session_state['feedback'] = {}

    # In the Tinder-style swipe interface, after each recommendation:
    if idx < len(recs):
        anime = recs[idx]
        st.subheader(anime['title'])
        st.write(f"Genres: {anime.get('genres', '')}")
        st.write(f"Score: {anime.get('score', 'N/A')}")
        st.write(anime.get('synopsis', ''))
        st.image(anime.get('image_url', ''), width=200)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("👍 To Watch"):
                st.session_state['to_watch'].append(anime)
                st.session_state['rec_index'] += 1
                st.session_state['feedback'][anime['title']] = 'to_watch'
        with col2:
            if st.button("👎 Not Interested"):
                st.session_state['not_interested'].append(anime)
                st.session_state['rec_index'] += 1
                st.session_state['feedback'][anime['title']] = 'not_interested'
        with col3:
            if st.button("✅ Watched"):
                st.session_state['watched'].append(anime)
                st.session_state['rec_index'] += 1
                st.session_state['feedback'][anime['title']] = 'watched'
        with col4:
            feedback = st.radio("Rate this recommendation:", ["👍 Like", "👎 Dislike", "🤷 Neutral"], key=f'fb_{idx}')
            st.session_state['feedback'][anime['title']] = feedback
    else:
        # At the end, show feedback summary
        st.success("No more recommendations! Reload or try new preferences.")
        st.write("**To Watch List:**", [a['title'] for a in st.session_state['to_watch']])
        st.write("**Watched List:**", [a['title'] for a in st.session_state['watched']])
        st.write("**Not Interested:**", [a['title'] for a in st.session_state['not_interested']])
        st.write("**Your Feedback:**")
        st.json(st.session_state['feedback'])

# Load ML KNN model and features
@st.cache_resource
def load_knn_model():
    knn = joblib.load('data/knn_model.joblib')
    scaler = joblib.load('data/knn_scaler.joblib')
    features_df = pd.read_csv('data/mal_anime_features.csv')
    return knn, scaler, features_df

knn, scaler, features_df = load_knn_model()

st.header('🔎 Fast ML-based Anime Recommendations')
# User selects a reference anime from the dataset
titles = pd.read_csv('data/mal_anime_clean.csv')['title'].tolist()
selected_title = st.selectbox('Pick an anime you like (from dataset):', titles)
if st.button('Recommend similar anime (ML KNN)'):
    idx = features_df.index[features_df['mal_id'] == int(pd.read_csv('data/mal_anime_clean.csv').set_index('title').loc[selected_title]['mal_id'])][0]
    # Only use numeric columns for KNN (as in train_knn_model.py)
    ignore_cols = ['mal_id', 'score']
    # Strictly match the dtype filter from train_knn_model.py
    feature_cols = [c for c in features_df.columns if c not in ignore_cols and features_df[c].dtype in [np.int64, np.float64, np.int32, np.float32]]
    X = features_df[feature_cols]
    idx = features_df.index[features_df['mal_id'] == int(pd.read_csv('data/mal_anime_clean.csv').set_index('title').loc[selected_title]['mal_id'])][0]
    sample = X.iloc[idx].values.reshape(1, -1)
    sample_scaled = scaler.transform(sample)
    dists, indices = knn.kneighbors(sample_scaled, n_neighbors=6)
    st.subheader('Top Recommendations:')
    clean_df = pd.read_csv('data/mal_anime_clean.csv').set_index('mal_id')
    for i, rec_idx in enumerate(indices[0][1:]):
        rec_id = features_df.iloc[rec_idx]['mal_id']
        rec = clean_df.loc[rec_id]
        st.markdown(f"**{i+1}. {rec['title']}**  ")
        st.write(f"Genres: {rec['genres']}")
        st.write(f"Score: {rec['score']}")
        st.write(rec['synopsis'])
        if pd.notna(rec['image_url']) and rec['image_url']:
            st.image(rec['image_url'], width=200)
        st.markdown('---')

st.markdown("---")
st.caption("Built with Streamlit. Powered by Jikan (MyAnimeList API). Content-based recommendations.")
