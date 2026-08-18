import os
from pathlib import Path
import psycopg
from dotenv import load_dotenv

# project root
BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env", override=True)

# postgreSQL connection information
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST_OVERRIDE") or os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")

conn = psycopg.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

print("PostgreSQL connection successful.")

with conn.cursor() as cur:
    # analytics schema
    cur.execute("""
        CREATE SCHEMA IF NOT EXISTS analytics;
    """)

    # 1- overview table
    cur.execute("""
        DROP TABLE IF EXISTS analytics.overview;

        CREATE TABLE analytics.overview AS
        SELECT
            COUNT(*) AS total_plays,
            ROUND(SUM(duration_ms)::numeric / 60000, 2) AS total_minutes,
            COUNT(DISTINCT track_id) AS unique_tracks,
            COUNT(DISTINCT artist_name) AS unique_artists,
            MIN(played_at) AS first_play,
            MAX(played_at) AS last_play
        FROM raw.plays;
    """)

    # 2- top tracks table
    cur.execute("""
        DROP TABLE IF EXISTS analytics.top_tracks;

        CREATE TABLE analytics.top_tracks AS
        SELECT
            track_id,
            track_name,
            artist_name,
            album_name,
            COUNT(*) AS play_count,
            ROUND(SUM(duration_ms)::numeric / 60000, 2) AS total_minutes,
            MAX(played_at) AS last_played_at
        FROM raw.plays
        GROUP BY
            track_id,
            track_name,
            artist_name,
            album_name;
    """)

    # 3- top artists table
    cur.execute("""
        DROP TABLE IF EXISTS analytics.top_artists;

        CREATE TABLE analytics.top_artists AS
        SELECT
            artist_name,
            COUNT(*) AS play_count,
            COUNT(DISTINCT track_id) AS unique_tracks,
            ROUND(SUM(duration_ms)::numeric / 60000, 2) AS total_minutes,
            MAX(played_at) AS last_played_at
        FROM raw.plays
        GROUP BY artist_name;
    """)

    # 4- daily stats table
    cur.execute("""
        DROP TABLE IF EXISTS analytics.daily_stats;

        CREATE TABLE analytics.daily_stats AS
        SELECT
            played_at::date AS listening_date,
            COUNT(*) AS play_count,
            COUNT(DISTINCT track_id) AS unique_tracks,
            COUNT(DISTINCT artist_name) AS unique_artists,
            ROUND(SUM(duration_ms)::numeric / 60000, 2) AS total_minutes
        FROM raw.plays
        GROUP BY played_at::date;
    """)

conn.commit()
conn.close()

print("Transformation completed successfully.")
print("Created tables:")
print("- analytics.overview")
print("- analytics.top_tracks")
print("- analytics.top_artists")
print("- analytics.daily_stats")