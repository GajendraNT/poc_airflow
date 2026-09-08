from fastapi import APIRouter, HTTPException

from app.services.airflow_service import AirflowService


router = APIRouter()

airflow_service = AirflowService()


@router.post("/deploy/{deployment_id}")
def deploy(deployment_id: str):

    try:
        dag_id = airflow_service.create_dag(deployment_id)

        return {
            "message": "Deployment DAG created successfully",
            "deployment_id": deployment_id,
            "dag_id": dag_id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
