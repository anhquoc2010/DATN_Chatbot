import datetime as _dt
from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship

from app.models.base import Base

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    province = Column(String, nullable=False)
    district = Column(String, nullable=False)
    ward = Column(String, nullable=False)
    address = Column(String, nullable=False)
    location = Column(JSON, nullable=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    description = Column(Text, nullable=False)
    register_link = Column(String, nullable=True)
    donation_method = Column(Integer, default=1, nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    deleted_at = Column(DateTime, default=None, nullable=True)
    created_at = Column(DateTime, default=_dt.datetime.now)
    updated_at = Column(DateTime, default=_dt.datetime.now, onupdate=_dt.datetime.now)

    # Relationships
    organization = relationship("Organization", back_populates="campaigns")
