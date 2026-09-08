from fastapi import FastAPI

from app.api.deploy import router as deploy_router


app = FastAPI(
    title="Deployment Service",
    version="1.0.0",
)


app.include_router(
    deploy_router,
    prefix="/api",
)


@app.get("/health")
def health():
    return {"status": "ok"}
