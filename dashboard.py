import os
import html
import pandas as pd
import plotly.express as px
import psycopg
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")

def get_connection():
    return psycopg.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

st.set_page_config(
    page_title="My Spotify Wrapped",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
<style>

.stApp {
    background-color: #F7F2EE;
    color: #111111;
    font-family: Helvetica, Arial, sans-serif;
}

html, body, [class*="css"] {
    font-family: Helvetica, Arial, sans-serif;
}

.block-container {
    max-width: 1250px;
    padding-top: 3rem;
    padding-bottom: 5rem;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

.hero-label {
    font-size: 12px;
    letter-spacing: 3px;
    font-weight: 600;
    color: #B48D98;
    margin-bottom: 15px;
}

.hero-title {
    font-size: 66px;
    line-height: 1.02;
    font-weight: 700;
    letter-spacing: -3px;
    color: #111111;
    margin-bottom: 15px;
}

.hero-description {
    font-size: 18px;
    color: #70676A;
    margin-bottom: 45px;
}

.metric-card {
    background-color: #FFF9F7;
    border: 1px solid #EADDDD;
    border-radius: 20px;
    padding: 28px;
    min-height: 145px;
}

.metric-label {
    font-size: 11px;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    color: #AA8791;
    font-weight: 600;
    margin-bottom: 20px;
}

.metric-value {
    font-size: 40px;
    font-weight: 700;
    letter-spacing: -1.5px;
    color: #111111;
}

.section-label {
    margin-top: 58px;
    margin-bottom: 8px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2.2px;
    text-transform: uppercase;
    color: #B48D98;
}

.section-title {
    font-size: 34px;
    font-weight: 700;
    letter-spacing: -1.3px;
    color: #111111;
    margin-bottom: 25px;
}

.top-artist-card {
    background-color: #F4E1E6;
    border-radius: 26px;
    padding: 48px;
    margin-top: 15px;
    margin-bottom: 10px;
    border: 1px solid #ECD5DB;
}

.top-artist-small {
    font-size: 11px;
    letter-spacing: 2.2px;
    font-weight: 600;
    color: #9B7580;
    text-transform: uppercase;
    margin-bottom: 18px;
}

.top-artist-name {
    font-size: 52px;
    font-weight: 700;
    letter-spacing: -2.5px;
    color: #111111;
    margin-bottom: 12px;
}

.top-artist-stat {
    font-size: 15px;
    color: #655B5E;
}

.track-row {
    display: flex;
    align-items: center;
    width: 100%;
    padding: 18px 4px;
    border-bottom: 1px solid #E6DADA;
    box-sizing: border-box;
}

.track-number {
    width: 48px;
    min-width: 48px;
    font-size: 13px;
    color: #C19CA6;
    font-weight: 600;
}

.track-info {
    flex: 1;
    min-width: 0;
}

.track-name {
    font-size: 16px;
    font-weight: 600;
    color: #111111;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.track-artist {
    font-size: 13px;
    color: #776C70;
    margin-top: 4px;
}

.track-count {
    font-size: 13px;
    color: #776C70;
    padding-left: 15px;
    white-space: nowrap;
}

.footer-text {
    margin-top: 65px;
    padding-top: 25px;
    border-top: 1px solid #E1D6D5;
    font-family: Helvetica, Arial, sans-serif;
    font-size: 11px;
    color: #A99399;
    letter-spacing: 1.5px;
}

div[data-testid="stVerticalBlock"] {
    gap: 0.7rem;
}

@media (max-width: 800px) {

    .hero-title {
        font-size: 44px;
        letter-spacing: -2px;
    }

    .top-artist-name {
        font-size: 38px;
    }

    .metric-value {
        font-size: 32px;
    }

    .section-title {
        font-size: 28px;
    }
}

</style>
""",
    unsafe_allow_html=True
)

conn = get_connection()

overview = pd.read_sql(
    """
    SELECT *
    FROM analytics.overview
    """,
    conn
)

top_tracks = pd.read_sql(
    """
    SELECT *
    FROM analytics.top_tracks
    ORDER BY play_count DESC, total_minutes DESC
    LIMIT 10
    """,
    conn
)

top_artists = pd.read_sql(
    """
    SELECT *
    FROM analytics.top_artists
    ORDER BY play_count DESC, total_minutes DESC
    LIMIT 10
    """,
    conn
)

daily_stats = pd.read_sql(
    """
    SELECT *
    FROM analytics.daily_stats
    ORDER BY listening_date
    """,
    conn
)

conn.close()

row = overview.iloc[0]

st.markdown(
    """
<div class="hero-label">PERSONAL LISTENING REPORT</div>
<div class="hero-title">Your listening,<br>in numbers.</div>
<div class="hero-description">
A personal overview of your recent Spotify listening activity.
</div>
""",
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-label">Total Plays</div>'
        f'<div class="metric-value">{int(row["total_plays"])}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-label">Minutes Listened</div>'
        f'<div class="metric-value">{float(row["total_minutes"]):.1f}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-label">Unique Tracks</div>'
        f'<div class="metric-value">{int(row["unique_tracks"])}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-label">Unique Artists</div>'
        f'<div class="metric-value">{int(row["unique_artists"])}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

if not top_artists.empty:

    top_artist = top_artists.iloc[0]

    artist_name = html.escape(str(top_artist["artist_name"]))
    play_count = int(top_artist["play_count"])
    total_minutes = float(top_artist["total_minutes"])

    st.markdown(
        '<div class="section-label">Your favorite</div>'
        '<div class="section-title">Top artist</div>',
        unsafe_allow_html=True
    )

    top_artist_html = (
        '<div class="top-artist-card">'
        '<div class="top-artist-small">Most played artist</div>'
        f'<div class="top-artist-name">{artist_name}</div>'
        f'<div class="top-artist-stat">'
        f'{play_count} plays &nbsp;&nbsp; / &nbsp;&nbsp; '
        f'{total_minutes:.1f} minutes listened'
        '</div>'
        '</div>'
    )

    st.markdown(
        top_artist_html,
        unsafe_allow_html=True
    )


left_col, right_col = st.columns(
    [1, 1],
    gap="large"
)

with left_col:

    st.markdown(
        '<div class="section-label">Ranking</div>'
        '<div class="section-title">Top artists</div>',
        unsafe_allow_html=True
    )

    artist_chart = px.bar(
        top_artists.head(7),
        x="play_count",
        y="artist_name",
        orientation="h",
        labels={
            "play_count": "",
            "artist_name": ""
        }
    )

    artist_chart.update_traces(
        marker_color="#E8C8D0",
        hovertemplate="<b>%{y}</b><br>%{x} plays<extra></extra>"
    )

    artist_chart.update_layout(

        yaxis={
            "categoryorder": "total ascending",
            "showgrid": False,
            "tickfont": {
                "family": "Helvetica, Arial, sans-serif",
                "size": 13,
                "color": "#111111"
            }
        },

        xaxis={
            "showgrid": False,
            "showticklabels": False,
            "zeroline": False
        },

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        font={
            "family": "Helvetica, Arial, sans-serif",
            "color": "#111111"
        },

        margin=dict(
            l=0,
            r=10,
            t=10,
            b=10
        ),

        height=410
    )

    st.plotly_chart(
        artist_chart,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )

with right_col:

    st.markdown(
        '<div class="section-label">Ranking</div>'
        '<div class="section-title">Top tracks</div>',
        unsafe_allow_html=True
    )

    for index, track in top_tracks.head(7).reset_index(drop=True).iterrows():

        track_name = html.escape(str(track["track_name"]))
        track_artist = html.escape(str(track["artist_name"]))
        play_count = int(track["play_count"])

        track_html = (
            f'<div class="track-row">'
            f'<div class="track-number">{index + 1:02}</div>'
            f'<div class="track-info">'
            f'<div class="track-name">{track_name}</div>'
            f'<div class="track-artist">{track_artist}</div>'
            f'</div>'
            f'<div class="track-count">{play_count} plays</div>'
            f'</div>'
        )

        st.markdown(
            track_html,
            unsafe_allow_html=True
        )

st.markdown(
    '<div class="section-label">Over time</div>'
    '<div class="section-title">Listening activity</div>',
    unsafe_allow_html=True
)

daily_chart = px.area(
    daily_stats,
    x="listening_date",
    y="play_count",
    labels={
        "listening_date": "",
        "play_count": ""
    }
)

daily_chart.update_traces(

    line=dict(
        color="#D9B8C0",
        width=3
    ),

    fillcolor="rgba(244, 225, 230, 0.70)",

    hovertemplate=(
        "<b>%{x}</b><br>"
        "%{y} plays"
        "<extra></extra>"
    )
)

daily_chart.update_layout(

    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",

    font={
        "family": "Helvetica, Arial, sans-serif",
        "color": "#111111"
    },

    xaxis={
        "showgrid": False,
        "title": None,
        "tickfont": {
            "color": "#736A6C"
        }
    },

    yaxis={
        "showgrid": True,
        "gridcolor": "#E9DFDD",
        "zeroline": False,
        "title": None,
        "tickfont": {
            "color": "#736A6C"
        }
    },

    margin=dict(
        l=0,
        r=0,
        t=20,
        b=0
    ),

    height=400
)

st.plotly_chart(
    daily_chart,
    use_container_width=True,
    config={
        "displayModeBar": False
    }
)

st.markdown(
    """
<div class="footer-text">
SPOTIFY LISTENING ANALYTICS · AIRFLOW · POSTGRESQL · STREAMLIT
</div>
""",
    unsafe_allow_html=True
)