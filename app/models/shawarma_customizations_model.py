from sqlalchemy import Integer, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure import Base


class ShawarmaCustomizations(Base):
    __tablename__ = "shawarma_customizations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_profile.id"), nullable=False, index=True)
    shawerma_id: Mapped[int] = mapped_column(Integer, ForeignKey("shawerma_type.id"), nullable=False, index=True)
    ingredient_id: Mapped[list[int]] = mapped_column(JSON, nullable=True)
