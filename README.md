# Deployment Service

A small FastAPI service that generates Airflow DAG files on demand. Each call
to the deploy endpoint writes a new DAG file to disk; Airflow (running
separately) picks it up, parses it, and shows it in the UI.

## Architecture

```
Client → FastAPI (app/api/deploy.py)
             → AirflowService.create_dag()
                   → writes app/templates/dag_template.py rendered DAG
                     to <AIRFLOW_DAG_DIR>/deployment_<id>.py
                                   ↓ (shared volume / folder)
                          Airflow scheduler & webserver
                                   → parses + serializes DAG
                                   → visible in Airflow UI (localhost:8080)
```

The FastAPI app never talks to Airflow over the network — it only writes
Python files into a directory. Airflow discovers new DAGs on its own polling
interval (`AIRFLOW__SCHEDULER__DAG_DIR_LIST_INTERVAL`, set to 5s in
`docker-compose.yml`).

This means the FastAPI process and Airflow just need to agree on **the same
directory on disk** for DAGs — it doesn't matter whether the FastAPI process
runs in Docker or on your host, as long as that directory maps to Airflow's
`/opt/airflow/dags/generated` inside its containers.

## Prerequisites

- Docker + Docker Compose
- Python 3.12 (for running the backend locally)

## Option A: Run everything in Docker (backend + Airflow)

```bash
docker compose up -d
```

This starts:

| Service               | Purpose                                  | Port |
|-----------------------|-------------------------------------------|------|
| `postgres`             | Airflow metadata DB                       | -    |
| `airflow-init`         | Runs migrations + creates admin user      | -    |
| `airflow-webserver`    | Airflow UI                                | 8080 |
| `airflow-scheduler`    | Parses DAGs, schedules runs               | -    |
| `api`                  | This FastAPI deployment service           | 8000 |

- Airflow UI: http://localhost:8080 (user: `admin`, password: `admin`)
- API: http://localhost:8000

Skip to [Using the API](#using-the-api).

## Option B: Run the backend locally, Airflow in Docker

This is useful when you're actively developing the FastAPI service and want
fast reload / debugging without rebuilding the Docker image each time.

### 1. Start only the Airflow stack

Don't start the `api` service — just the Airflow/Postgres pieces:

```bash
docker compose up -d postgres airflow-init airflow-webserver airflow-scheduler
```

Wait for `airflow-init` to finish (it exits after creating the DB schema and
the admin user), then confirm the webserver + scheduler are healthy:

```bash
docker compose ps
```

Airflow UI: http://localhost:8080 (`admin` / `admin`).

### 2. Set up the backend locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Point the backend at the same DAG folder Airflow is watching

Docker mounts the host folder `./airflow/dags` to `/opt/airflow/dags` inside
the Airflow containers. When the backend runs on your host (not in Docker),
it must write into that same host folder — use an **absolute path**:

```bash
export AIRFLOW_DAG_DIR="$(pwd)/airflow/dags/generated"
```

(`AirflowService` defaults to `/opt/airflow/dags/generated`, which only
exists *inside* a container — you must override it when running the backend
locally.)

### 4. Run the backend

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API is now available at http://localhost:8000, and any DAG it generates
lands in `./airflow/dags/generated/`, which the Dockerized Airflow scheduler
is already watching.

## Using the API

Health check:

```bash
curl http://localhost:8000/health
```

Create a deployment DAG:

```bash
curl -X POST http://localhost:8000/api/deploy/1
```

```json
{
  "message": "Deployment DAG created successfully",
  "deployment_id": "1",
  "dag_id": "deployment_1"
}
```

The new DAG (`deployment_1`) should appear in the Airflow UI within a few
seconds (scheduler re-scans the DAGs folder every 5 seconds).

## Troubleshooting

**DAG doesn't show up in the Airflow UI:**

- Give it a few seconds — the scheduler needs to parse and serialize the new
  file before the webserver (which reads from the metadata DB, not disk)
  will show it.
- Confirm the backend is writing to the folder Airflow actually mounts. If
  running the backend locally, double-check `AIRFLOW_DAG_DIR` is set to the
  **absolute host path** of `./airflow/dags/generated`.
- Check for import errors:
  ```bash
  docker exec deployment-service-airflow-scheduler-1 airflow dags list-import-errors
  ```
- List DAGs Airflow currently knows about:
  ```bash
  docker exec deployment-service-airflow-scheduler-1 airflow dags list
  ```

**Resetting everything:**

```bash
docker compose down -v
```

This drops the Postgres volume (Airflow metadata) as well as generated DAG
logs/plugins volumes. Generated DAG files under `./airflow/dags/generated`
are on the host and are **not** removed by this command — delete them
manually if you want a clean slate.
