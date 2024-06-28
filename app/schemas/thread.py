# import datetime as _dt
# from sqlalchemy import Boolean, Column, Integer, String, DateTime
# from sqlalchemy.orm import relationship

# from app.models.base import Base

# class Threads(Base):
#     __tablename__ = "thread"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String)
#     description = Column(String)
#     organization_id = Column(Integer)
#     user_id = Column(Integer)
#     created_at = Column(DateTime, default=_dt.datetime.now())
#     updated_at = Column(DateTime, default=_dt.datetime.now())

#     message = relationship("Messages", back_populates="thread")

from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class ThreadBase(BaseModel):
    title: Optional[str]
    description: Optional[str]
    organization_id: Optional[int]
    user_id: Optional[int]

class ThreadCreate(ThreadBase):
    pass

class ThreadUpdate(ThreadBase):
    pass

class ThreadOut(ThreadBase):
    id: int 
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    class Config:
        from_attributes = True

class ThreadInDB(ThreadBase):
    pass