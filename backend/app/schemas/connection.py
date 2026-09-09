import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ConnectionCreate(BaseModel):
    connection_name: str
    host_port: str
    username: str
    password: str
    description: str | None = None
    database: str


class ConnectionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    connection_name: str
    host_port: str
    username: str
    description: str | None
    database: str
    created_at: datetime
    updated_at: datetime
