import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.connection import Connection
from app.schemas.connection import ConnectionCreate, ConnectionResponse

router = APIRouter()


@router.post("/connections", response_model=ConnectionResponse, status_code=201)
def create_connection(payload: ConnectionCreate, db: Session = Depends(get_db)):
    connection = Connection(**payload.model_dump())

    db.add(connection)
    db.commit()
    db.refresh(connection)

    return connection


@router.get("/connections/{connection_id}", response_model=ConnectionResponse)
def get_connection(connection_id: uuid.UUID, db: Session = Depends(get_db)):
    connection = db.get(Connection, connection_id)

    if connection is None:
        raise HTTPException(status_code=404, detail="Connection not found")

    return connection


@router.get("/connections", response_model=list[ConnectionResponse])
def list_connections(db: Session = Depends(get_db)):
    return db.execute(select(Connection)).scalars().all()
