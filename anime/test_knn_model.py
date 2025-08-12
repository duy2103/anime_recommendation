import pandas as pd
import joblib
import numpy as np

# Load data and model
features_path = "data/mal_anime_features.csv"
model_path = "data/knn_model.joblib"
scaler_path = "data/knn_scaler.joblib"
df = pd.read_csv(features_path)
knn = joblib.load(model_path)
scaler = joblib.load(scaler_path)

# Pick a sample anime (first row) to test
sample_idx = 0
ignore_cols = ['mal_id', 'score']
# Only use numeric columns for KNN (as in train_knn_model.py)
feature_cols = [c for c in df.columns if c not in ignore_cols and df[c].dtype in [np.int64, np.float64, np.int32, np.float32]]
sample = df.iloc[sample_idx][feature_cols].values.reshape(1, -1)
sample_scaled = scaler.transform(sample)

# Find nearest neighbors
n_neighbors = 5
dists, indices = knn.kneighbors(sample_scaled, n_neighbors=n_neighbors)

print(f"Sample anime: {df.iloc[sample_idx]['title'] if 'title' in df.columns else df.iloc[sample_idx]['mal_id']}")
print("Nearest neighbors:")
for i, idx in enumerate(indices[0]):
    print(f"{i+1}. {df.iloc[idx]['title'] if 'title' in df.columns else df.iloc[idx]['mal_id']} (distance: {dists[0][i]:.4f})")
