import pandas as pd
import numpy as np
import re
import logging
from src.feature_engineering import engineer_features

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Load cleaned data
input_path = "data/mal_anime_clean.csv"
try:
    df = pd.read_csv(input_path)
except Exception as e:
    logging.error(f"Failed to load {input_path}: {e}")
    raise

# Feature engineering
try:
    ml_df = engineer_features(df)
except Exception as e:
    logging.error(f"Feature engineering failed: {e}")
    raise

# Save to CSV
try:
    ml_df.to_csv("data/mal_anime_features.csv", index=False)
    print(f"Feature-engineered data saved to data/mal_anime_features.csv. Shape: {ml_df.shape}")
except Exception as e:
    logging.error(f"Failed to save features CSV: {e}")
    raise
