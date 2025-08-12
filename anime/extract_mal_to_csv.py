import requests
import pandas as pd
import time

# Jikan API endpoint for anime list
BASE_URL = "https://api.jikan.moe/v4/anime"

# Fields to extract
FIELDS = [
    'mal_id', 'title', 'type', 'source', 'score', 'synopsis', 'status', 'episodes', 'duration', 'rating',
    'genres', 'aired', 'images', 'popularity', 'members', 'favorites', 'url'
]

def fetch_anime_page(page, max_retries=5):
    url = f"{BASE_URL}?page={page}"
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=20)
            if response.status_code != 200:
                print(f"Error fetching page {page}: {response.status_code}")
                time.sleep(2 ** attempt)
                continue
            data = response.json().get('data', [])
            return data
        except Exception as e:
            print(f"Exception on page {page}, attempt {attempt+1}: {e}")
            time.sleep(2 ** attempt)
    print(f"Failed to fetch page {page} after {max_retries} attempts. Skipping.")
    return []

def flatten_anime(anime):
    # Flatten genres, images, aired
    genres = ', '.join([g['name'] for g in anime.get('genres', [])])
    aired_from = anime.get('aired', {}).get('from', '')
    aired_to = anime.get('aired', {}).get('to', '')
    image_url = anime.get('images', {}).get('jpg', {}).get('large_image_url', '')
    return {
        'mal_id': anime.get('mal_id'),
        'title': anime.get('title'),
        'type': anime.get('type'),
        'source': anime.get('source'),
        'score': anime.get('score'),
        'synopsis': anime.get('synopsis'),
        'status': anime.get('status'),
        'episodes': anime.get('episodes'),
        'duration': anime.get('duration'),
        'rating': anime.get('rating'),
        'genres': genres,
        'aired_from': aired_from,
        'aired_to': aired_to,
        'image_url': image_url,
        'popularity': anime.get('popularity'),
        'members': anime.get('members'),
        'favorites': anime.get('favorites'),
        'url': anime.get('url'),
    }

def main():
    all_anime = []
    page = 1
    max_pages = 10000  # Set a high limit; will break when no more data
    while True:
        print(f"Fetching page {page}...")
        data = fetch_anime_page(page)
        if not data:
            break
        for anime in data:
            all_anime.append(flatten_anime(anime))
        page += 1
        time.sleep(0.5)  # Respect Jikan rate limit
    print(f"Fetched {len(all_anime)} anime entries.")
    df = pd.DataFrame(all_anime)
    df.to_csv("data/mal_anime_full.csv", index=False)
    print("Saved to data/mal_anime_full.csv")

if __name__ == "__main__":
    main()
