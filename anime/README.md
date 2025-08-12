# Anime Recommendation System (MyAnimeList)

A hybrid anime recommender system using MyAnimeList data, featuring both content-based and machine learning (KNN) recommendations. Includes a modern Streamlit web app for user interaction, onboarding, and feedback collection.

## Features
- **KNN-based Recommendations:** Find similar anime using a K-Nearest Neighbors model trained on engineered features.
- **Content-based Filtering:** Personalized recommendations based on genres, types, and user preferences.
- **Unified Onboarding:** Both new and returning users can specify genres, types, eras (multi-select), themes, tone, age rating, language, minimum episodes, and minimum minutes per episode for recommendations.
- **Streamlit UI:** Interactive web app for onboarding, recommendations, and feedback.
- **Feedback Loop:** Tinder-style swipe interface for collecting user feedback.
- **Automated Data Updates:** Data is automatically refreshed every 2 weeks via a cron job, and changes are auto-committed and pushed to GitHub.

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

### 5. Automated Data Updates (Cron Job)

A cron job is set up to run every 2 weeks, automatically updating the anime data and pushing changes to GitHub. The script used is:

```zsh
./update_anime_data.sh
```

This script:
- Extracts the latest anime data from MyAnimeList (via Jikan API)
- Runs feature engineering
- Commits and pushes any data changes to your GitHub repository

You can find and edit the cron job with:
```zsh
crontab -e
```

Logs are saved to `data_update.log` in the project directory.

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
