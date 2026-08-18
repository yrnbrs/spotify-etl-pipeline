# Spotify ETL Pipeline

A data engineering project I built using my Spotify listening data.

The project gets recently played tracks from Spotify, loads them into PostgreSQL, runs the ETL process with Apache Airflow, and shows the results in a Streamlit dashboard.

## Live Demo

https://spotify-listening-dashboard.streamlit.app/

## Architecture

* Spotify API
* Python
* Apache Airflow
* PostgreSQL
* Analytics Tables
* Streamlit Dashboard

For the deployed dashboard, I use Neon PostgreSQL as the cloud database.

## Tech Stack

* Python
* Spotify Web API
* Apache Airflow
* PostgreSQL
* Docker
* Pandas
* SQLAlchemy
* Plotly
* Streamlit
* Neon

## How It Works

The Airflow pipeline has three main steps:

* extract_spotify_data
* load_to_postgres
* transform_to_analytics

**Extract:** Gets recently played tracks from Spotify.

**Load:** Stores the data in PostgreSQL and prevents duplicate records.

**Transform:** Creates analytics tables for the dashboard.

The dashboard currently shows:

* Total plays
* Listening time
* Unique tracks
* Unique artists
* Top artists
* Top tracks
* Daily listening activity

## Project Structure

* airflow
* sql
* extract.py
* load.py
* transform.py
* dashboard.py
* docker-compose.yml
* requirements.txt
* README.md

## Run Locally

Clone the project:

```bash
git clone https://github.com/yrnbrs/spotify-etl-pipeline.git
cd spotify-etl-pipeline
```

Install the requirements:

```bash
pip install -r requirements.txt
```

Start PostgreSQL:

```bash
docker compose up -d
```

Run the dashboard:

```bash
streamlit run dashboard.py
```

The dashboard will be available at:

```text
http://localhost:8501
```

## Airflow

Start Airflow from the `airflow` folder:

```bash
cd airflow
docker compose up -d
```

Airflow UI:

```text
http://localhost:8080
```

The DAG name is:

```text
spotify_etl_pipeline
```

## Dashboard

Live version:

https://spotify-listening-dashboard.streamlit.app/

## Author

Yaren Barış