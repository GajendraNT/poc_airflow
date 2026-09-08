def generate_dag(
    dag_id: str,
    deployment_id: str,
) -> str:

    return f'''
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def deploy():
    print("Deploying deployment: {deployment_id}")


with DAG(
    dag_id="{dag_id}",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    deploy_task = PythonOperator(
        task_id="deploy",
        python_callable=deploy,
    )
'''
