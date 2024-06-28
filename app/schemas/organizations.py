# import datetime as _dt
# from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, ForeignKey, Float
# from sqlalchemy.orm import relationship
# from geoalchemy2 import Geometry

# from app.models.base import Base

# class Organization(Base):
#     __tablename__ = "organizations"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, unique=True, nullable=False)
#     address = Column(String, nullable=False)
#     phone_number = Column(String(20), unique=True, nullable=False)
#     description = Column(Text, nullable=True)
#     avatar = Column(String, nullable=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
#     deleted_at = Column(DateTime, default=None, nullable=True)
#     created_at = Column(DateTime, default=_dt.datetime.now)
#     updated_at = Column(DateTime, default=_dt.datetime.now, onupdate=_dt.datetime.now)

#     # Relationships
#     campaigns = relationship("Campaign", back_populates="organization")

from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class OrganizationBase(BaseModel):
    name: str
    address: str
    phone_number: str
    description: Optional[str] = None
    avatar: Optional[str] = None
    user_id: Optional[int] = None

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationUpdate(OrganizationBase):
    pass

class OrganizationOut(OrganizationBase):
    id: int
    deleted_at: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    class Config:
        from_attributes = True

class OrganizationInDB(OrganizationBase):
    pass