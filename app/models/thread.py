import datetime as _dt
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.models.base import Base

class Thread(Base):
    __tablename__ = "thread"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    organization_id = Column(Integer)
    user_id = Column(Integer)
    created_at = Column(DateTime, default=_dt.datetime.now())
    updated_at = Column(DateTime, default=_dt.datetime.now())

    message = relationship("Message", back_populates="thread")