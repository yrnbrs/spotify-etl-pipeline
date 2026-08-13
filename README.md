# Spotify ETL Pipeline

Project Overview

Architecture
Spotify API -> Python -> JSON -> PostgreSQL

Tech Stack
- Python
- Spotify Web API
- PostgreSQL
- Docker
- Git

How It Works
1. Extract recently played tracks
2. Store raw JSON
3. Load records into PostgreSQL
4. Prevent duplicates with an idempotent load

Project Structure

Setup

Environment Variables

Running the Pipeline

Roadmap
- Airflow
- dbt
- Analytics
- Cloud deployment
