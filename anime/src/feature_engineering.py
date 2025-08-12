"""
Reusable feature engineering functions for anime recommender.
"""
import pandas as pd
import numpy as np
import re
from .config import GENRES, TYPES, SOURCES, STATUSES

def parse_duration(s):
    if pd.isna(s):
        return 0
    m = re.search(r'(\d+) min', str(s))
    return int(m.group(1)) if m else 0

def engineer_features(df):
    # One-hot encode 'type', 'source', 'status'
    type_dummies = pd.get_dummies(df['type'], prefix='type')
    source_dummies = pd.get_dummies(df['source'], prefix='source')
    status_dummies = pd.get_dummies(df['status'], prefix='status')
    # Multi-hot encode 'genres'
    for genre in GENRES:
        df[f'genre_{genre}'] = df['genres'].apply(lambda x: int(genre in str(x).split(', ')))
    # Numeric features
    df['episodes'] = pd.to_numeric(df['episodes'], errors='coerce').fillna(0)
    df['popularity'] = pd.to_numeric(df['popularity'], errors='coerce').fillna(0)
    df['members'] = pd.to_numeric(df['members'], errors='coerce').fillna(0)
    df['favorites'] = pd.to_numeric(df['favorites'], errors='coerce').fillna(0)
    df['duration_min'] = df['duration'].apply(parse_duration)
    df['year'] = pd.to_datetime(df['aired_from'], errors='coerce').dt.year.fillna(0).astype(int)
    # Drop unused columns for ML
    ml_df = df.drop(columns=['title','synopsis','image_url','url','genres','duration','aired_from','aired_to'])
    ml_df = pd.concat([ml_df, type_dummies, source_dummies, status_dummies], axis=1)
    return ml_df
