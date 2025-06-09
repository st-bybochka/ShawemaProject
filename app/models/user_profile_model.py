from sqlalchemy import Integer, String, DateTime
from sqlalchemy.sql import func
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure import Base

class UserProfile(Base):
    __tablename__ = "user_profile"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)
    login_attempts: Mapped[int] = mapped_column(Integer, default=0)
    block_until: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=None)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)