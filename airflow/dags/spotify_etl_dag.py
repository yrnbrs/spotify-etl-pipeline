from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator


with DAG(
    dag_id="spotify_etl_pipeline",
    start_date=datetime(2026, 8, 1),
    schedule="0 * * * *",
    catchup=False,
    tags=["spotify", "etl"],
) as dag:

    extract_spotify_data = BashOperator(
        task_id="extract_spotify_data",
        bash_command="python /opt/airflow/project/extract.py",
    )

    load_to_postgres = BashOperator(
        task_id="load_to_postgres",
        bash_command="python /opt/airflow/project/load.py",
    )

    transform_to_analytics = BashOperator(
        task_id="transform_to_analytics",
        bash_command="python /opt/airflow/project/transform.py",
    )

    extract_spotify_data >> load_to_postgres >> transform_to_analytics