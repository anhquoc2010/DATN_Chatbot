# import datetime as _dt
# from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, ForeignKey, Float
# from sqlalchemy.orm import relationship
# from geoalchemy2 import Geometry

# from app.models.base import Base

# class Campaign(Base):
#     __tablename__ = "campaigns"

    # id = Column(Integer, primary_key=True, index=True)
    # name = Column(String, nullable=False)
    # city = Column(String, nullable=False)
    # district = Column(String, nullable=False)
    # ward = Column(String, nullable=False)
    # address = Column(String, nullable=False)
    # coordinate = Column(JSON, nullable=True)
    # start_date = Column(DateTime, nullable=False)
    # end_date = Column(DateTime, nullable=False)
    # description = Column(Text, nullable=False)
    # register_link = Column(String, nullable=True)
    # donation_requirement = Column(Integer, default=1, nullable=False)
    # organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    # deleted_at = Column(DateTime, default=None, nullable=True)
    # created_at = Column(DateTime, default=_dt.datetime.now)
    # updated_at = Column(DateTime, default=_dt.datetime.now, onupdate=_dt.datetime.now)

#     # Relationships
#     organization = relationship("Organization", back_populates="campaigns")

from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class CampaignBase(BaseModel):
    name: Optional[str]
    city: Optional[str]
    district: Optional[str]
    ward: Optional[str]
    address: Optional[str]
    coordinate: Optional[dict]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    description: Optional[str]
    register_link: Optional[str]
    donation_requirement: Optional[str]
    organization_id: Optional[int]

class CampaignCreate(CampaignBase):
    pass

class CampaignUpdate(CampaignBase):
    pass

class CampaignOut(CampaignBase):
    id: int
    deleted_at: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    class Config:
        from_attributes = True

class CampaignInDB(CampaignBase):
    pass