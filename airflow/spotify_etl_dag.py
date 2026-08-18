from datetime import datetime, timedelta

from airflow.sdk import dag, task


default_args = {
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


@dag(
    dag_id="spotify_etl_pipeline",
    # Spotify's recently-played endpoint only returns your last 50 tracks,
    # so this needs to run often enough that a heavy listening session
    # never pushes plays out of that window before we capture them.
    schedule="0 */3 * * *",  # every 3 hours
    start_date=datetime(2026, 8, 1),
    catchup=False,
    default_args=default_args,
    tags=["spotify", "etl"],
)
def spotify_etl_pipeline():

    @task.bash
    def extract_spotify_data():
        return "python /opt/airflow/project/extract.py"

    @task.bash
    def load_to_postgres():
        return "python /opt/airflow/project/load.py"

    @task.bash
    def transform_analytics():
        return "python /opt/airflow/project/transform.py"

    extract_task = extract_spotify_data()
    load_task = load_to_postgres()
    transform_task = transform_analytics()

    extract_task >> load_task >> transform_task


spotify_etl_pipeline()