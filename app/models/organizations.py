import datetime as _dt
from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from app.models.base import Base

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    avatar = Column(String, nullable=True)
    user_id = Column(Integer, nullable=True)
    deleted_at = Column(DateTime, default=None, nullable=True)
    created_at = Column(DateTime, default=_dt.datetime.now)
    updated_at = Column(DateTime, default=_dt.datetime.now, onupdate=_dt.datetime.now)

    # Relationships
    campaigns = relationship("Campaign", back_populates="organization")
