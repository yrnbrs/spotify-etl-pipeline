import os
import json
from datetime import datetime
from pathlib import Path

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

# 1- load .env file and get Spotify credentials
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env", override=True)

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

# check if the credentials are loaded correctly
print("Client ID found:", bool(CLIENT_ID))
print("Client Secret found:", bool(CLIENT_SECRET))
print("Redirect URI:", REDIRECT_URI)

# 2- connect to Spotify API using Spotipy
spotify = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-read-recently-played"
    )
)

# 3- get recently played tracks from Spotify
print("Fetching data from Spotify...")

data = spotify.current_user_recently_played(limit=50)

# 4- create data/raw directory
raw_data_dir = BASE_DIR / "data" / "raw"
raw_data_dir.mkdir(parents=True, exist_ok=True)

# 5- save JSON file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

file_path = raw_data_dir / f"recently_played_{timestamp}.json"

with open(file_path, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print("Spotify data saved successfully:")
print(file_path)