import os
from pathlib import Path

from app.templates.dag_template import generate_dag


class AirflowService:
    def __init__(self):

        self.dag_directory = Path(
            os.getenv("AIRFLOW_DAG_DIR", "/opt/airflow/dags/generated")
        )

        self.dag_directory.mkdir(parents=True, exist_ok=True)

    def create_dag(self, deployment_id: str) -> str:

        dag_id = f"deployment_{deployment_id}"

        dag_content = generate_dag(
            dag_id=dag_id,
            deployment_id=deployment_id,
        )

        dag_file = self.dag_directory / f"{dag_id}.py"

        dag_file.write_text(dag_content, encoding="utf-8")

        return dag_id
