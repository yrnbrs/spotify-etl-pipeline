import os
import json
from pathlib import Path

import psycopg
from dotenv import load_dotenv
# 1- find project root directory and load .env file
BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env", override=True)

# 2- get PostgreSQL credentials from .env
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST_OVERRIDE") or os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")

# 3- find the most recently created JSON file
raw_data_dir = BASE_DIR / "data" / "raw"

json_files = list(raw_data_dir.glob("recently_played_*.json"))

if not json_files:
    raise FileNotFoundError("No JSON file found in the data/raw directory.")

latest_file = max(json_files, key=lambda file: file.stat().st_mtime)

print(f"JSON file being read: {latest_file.name}")

# 4- load JSON file into Python
with open(latest_file, "r", encoding="utf-8") as file:
    data = json.load(file)

# 5- connect to PostgreSQL
connection = psycopg.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

inserted_count = 0
duplicate_count = 0

# 6- handle Spotify records one by one and insert into PostgreSQL
with connection:

    with connection.cursor() as cursor:

        for item in data["items"]:

            track = item["track"]

            played_at = item["played_at"]
            track_id = track["id"]
            track_name = track["name"]

            artist_name = track["artists"][0]["name"]

            album_id = track["album"]["id"]
            album_name = track["album"]["name"]

            duration_ms = track["duration_ms"]
            explicit = track["explicit"]

            spotify_url = track["external_urls"]["spotify"]

            # 7. PostgreSQL INSERT
            cursor.execute(
                """
                INSERT INTO raw.plays (
                    played_at,
                    track_id,
                    track_name,
                    artist_name,
                    album_id,
                    album_name,
                    duration_ms,
                    explicit,
                    spotify_url
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s
                )
                ON CONFLICT (track_id, played_at)
                DO NOTHING
                """,
                (
                    played_at,
                    track_id,
                    track_name,
                    artist_name,
                    album_id,
                    album_name,
                    duration_ms,
                    explicit,
                    spotify_url
                )
            )

            if cursor.rowcount == 1:
                inserted_count += 1
            else:
                duplicate_count += 1

print()
print("Upload completed.")
print(f"New records inserted: {inserted_count}")
print(f"Duplicates skipped: {duplicate_count}")