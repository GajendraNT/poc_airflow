from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import BaseModel


class Connection(BaseModel):
    __tablename__ = "connection"

    connection_name: Mapped[str] = mapped_column(String(255), nullable=False)
    host_port: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    database: Mapped[str] = mapped_column(String(255), nullable=False)
