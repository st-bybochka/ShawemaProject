from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure import Base

class Ingredients(Base):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    is_base: Mapped[bool] = mapped_column(Boolean, default=False)