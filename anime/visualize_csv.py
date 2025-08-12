import pandas as pd
import streamlit as st

st.title("MAL Anime CSV Visualizer")

csv_path = "data/mal_anime_full.csv"

# Load the CSV
@st.cache_data

def load_csv():
    return pd.read_csv(csv_path)

df = load_csv()

st.write(f"Loaded {len(df)} anime entries.")

# Show the dataframe
st.dataframe(df, use_container_width=True)

# Show some basic stats
st.subheader("Basic Statistics")
st.write(df.describe(include='all'))

# Genre distribution
if 'genres' in df.columns:
    st.subheader("Top Genres")
    from collections import Counter
    genre_counts = Counter()
    for genres in df['genres'].dropna():
        for g in str(genres).split(', '):
            genre_counts[g] += 1
    top_genres = genre_counts.most_common(20)
    st.bar_chart(pd.DataFrame(top_genres, columns=["Genre", "Count"]).set_index("Genre"))

# Score distribution
if 'score' in df.columns:
    st.subheader("Score Distribution")
    st.histogram(df['score'].dropna(), bins=20)
