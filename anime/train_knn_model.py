import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import numpy as np
import joblib

# Load feature data
input_path = "data/mal_anime_features.csv"
df = pd.read_csv(input_path)

# Select features for KNN (exclude id, score, and any non-numeric/categorical columns not encoded)
ignore_cols = ['mal_id', 'score']
# Only use numeric columns for KNN
feature_cols = [c for c in df.columns if c not in ignore_cols and df[c].dtype in [np.int64, np.float64, np.int32, np.float32]]
X = df[feature_cols]

# Standardize numeric features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train KNN model
knn = NearestNeighbors(n_neighbors=10, metric='euclidean')
knn.fit(X_scaled)

# Save model and scaler
joblib.dump(knn, 'data/knn_model.joblib')
joblib.dump(scaler, 'data/knn_scaler.joblib')
print("KNN model and scaler saved to data/knn_model.joblib and data/knn_scaler.joblib")
