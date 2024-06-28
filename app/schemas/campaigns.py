# import datetime as _dt
# from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, ForeignKey, Float
# from sqlalchemy.orm import relationship
# from geoalchemy2 import Geometry

# from app.models.base import Base

# class Campaign(Base):
#     __tablename__ = "campaigns"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     province = Column(String, nullable=False)
#     district = Column(String, nullable=False)
#     ward = Column(String, nullable=False)
#     address = Column(String, nullable=False)
#     location = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)  # Using GeoAlchemy for point
#     start_date = Column(DateTime, nullable=False)
#     end_date = Column(DateTime, nullable=False)
#     description = Column(Text, nullable=False)
#     register_link = Column(String, nullable=True)
#     donation_method = Column(Integer, default=1, nullable=False)
#     organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
#     deleted_at = Column(DateTime, default=None, nullable=True)
#     created_at = Column(DateTime, default=_dt.datetime.now)
#     updated_at = Column(DateTime, default=_dt.datetime.now, onupdate=_dt.datetime.now)

#     # Relationships
#     organization = relationship("Organization", back_populates="campaigns")

from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class CampaignBase(BaseModel):
    name: str
    province: str
    district: str
    ward: str
    address: str
    start_date: datetime
    l
    end_date: datetime
    description: str
    register_link: Optional[str] = None
    donation_method: int
    organization_id: int

class CampaignCreate(CampaignBase):
    pass

class CampaignUpdate(CampaignBase):
    pass

class CampaignOut(CampaignBase):
    id: int
    location: Optional[str]
    deleted_at: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    class Config:
        from_attributes = True

class CampaignInDB(CampaignBase):
    pass

