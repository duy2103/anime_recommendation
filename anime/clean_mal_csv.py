import pandas as pd

# Load the raw CSV
raw_path = "data/mal_anime_full.csv"
df = pd.read_csv(raw_path)

# Drop duplicates by mal_id or title
if 'mal_id' in df.columns:
    df = df.drop_duplicates(subset=['mal_id'])
else:
    df = df.drop_duplicates(subset=['title'])

# Drop rows with missing essential fields (title, genres, score)
df = df.dropna(subset=['title', 'genres', 'score'])

# Remove anime with score 0 or not rated
df = df[df['score'] > 0]

# Remove anime with no genres
df = df[df['genres'].str.strip() != '']

# Optionally, filter by type (e.g., only TV and Movie)
if 'type' in df.columns:
    df = df[df['type'].isin(['TV', 'Movie'])]

# Optionally, filter by year (aired_from)
if 'aired_from' in df.columns:
    df['year'] = pd.to_datetime(df['aired_from'], errors='coerce').dt.year
    df = df[(df['year'] >= 1980) & (df['year'] <= 2025)]

# Save cleaned data
clean_path = "data/mal_anime_clean.csv"
df.to_csv(clean_path, index=False)
print(f"Cleaned data saved to {clean_path}. {len(df)} entries remain.")
