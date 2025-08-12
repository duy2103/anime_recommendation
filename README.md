# Anime Recommendation System 

A hybrid anime recommender system using MyAnimeList data, featuring both content-based and machine learning (KNN) recommendations. Includes a modern Streamlit web app for user interaction, onboarding, and feedback collection.

## Features
- **KNN-based Recommendations:** Find similar anime using a K-Nearest Neighbors model trained on engineered features.
- **Content-based Filtering:** Personalized recommendations based on genres, types, and user preferences.
- **Streamlit UI:** Interactive web app for onboarding, recommendations, and feedback.
- **Feedback Loop:** Tinder-style swipe interface for collecting user feedback.

## Quickstart

### 1. Clone the repository
```zsh
git clone https://github.com/duy2103/anime_recommendation.git
cd anime_recommendation
```

### 2. Install dependencies
It is recommended to use a virtual environment (e.g., `venv` or `conda`).
```zsh
pip install -r requirements.txt
```

### 3. Prepare data and train the model
If not already present, generate features and train the KNN model:
```zsh
python feature_engineering.py
python train_knn_model.py
```

### 4. Run the Streamlit app
```zsh
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## Project Structure
- `app.py` — Main Streamlit app
- `train_knn_model.py` — KNN model training script
- `feature_engineering.py` — Feature engineering pipeline
- `test_knn_model.py` — Test script for KNN recommendations
- `data/` — Contains CSVs, model artifacts, and features
- `src/` — Core modules (recommender, config, data loader)

## Data Sources
- [MyAnimeList](https://myanimelist.net/) (via Jikan API)

## Requirements
- Python 3.8+
- See `requirements.txt` for full dependencies

## Author
[duy2103](https://github.com/duy2103)

## License
MIT License
