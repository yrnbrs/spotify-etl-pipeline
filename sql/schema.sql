CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.plays (
    id BIGSERIAL PRIMARY KEY,

    played_at TIMESTAMPTZ NOT NULL,

    track_id TEXT NOT NULL,
    track_name TEXT NOT NULL,

    artist_name TEXT NOT NULL,

    album_id TEXT,
    album_name TEXT,

    duration_ms INTEGER,
    explicit BOOLEAN,

    spotify_url TEXT,

    loaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (track_id, played_at)
);