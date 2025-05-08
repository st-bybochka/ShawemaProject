from sqlalchemy import Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure import Base


class Shawerma(Base):
    __tablename__ = "shawerma_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    base_ingredients: Mapped[list[str]] = mapped_column(JSON)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
