import datetime as _dt
from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from app.models.base import Base

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    city = Column(String, nullable=True)
    district = Column(String, nullable=True)
    ward = Column(String, nullable=True)
    address = Column(String, nullable=True)
    coordinate = Column(JSON, nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    description = Column(Text, nullable=True)
    register_link = Column(String, nullable=True)
    donation_requirement = Column(String, nullable=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    deleted_at = Column(DateTime, default=None, nullable=True)
    created_at = Column(DateTime, default=_dt.datetime.now)
    updated_at = Column(DateTime, default=_dt.datetime.now, onupdate=_dt.datetime.now)

    # Relationships
    organization = relationship("Organization", back_populates="campaigns")
