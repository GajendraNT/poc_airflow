
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def deploy():
    print("Deploying deployment: 2")


with DAG(
    dag_id="deployment_2",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    deploy_task = PythonOperator(
        task_id="deploy",
        python_callable=deploy,
    )
