from sqlalchemy import Integer, String, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure import Base

class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    location: Mapped[str] = mapped_column(String(100), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    is_shop: Mapped[bool] = mapped_column(Boolean, default=False)