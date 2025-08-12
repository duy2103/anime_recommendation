#!/bin/zsh
# Update anime data from Jikan API and process features
cd "$(dirname "$0")"

# Extract latest anime data
echo "[Cron] Extracting latest anime data..."
python3 extract_mal_to_csv.py

# Clean and engineer features
echo "[Cron] Running feature engineering..."
python3 feature_engineering.py

echo "[Cron] Data update complete."

# Git commit and push
GIT_DATE=$(date '+%Y-%m-%d %H:%M:%S')
git add data/*.csv data/*.joblib
if ! git diff --cached --quiet; then
  git commit -m "[cron] Auto-update anime data: $GIT_DATE"
  git push origin main
else
  echo "[Cron] No data changes to commit."
fi
