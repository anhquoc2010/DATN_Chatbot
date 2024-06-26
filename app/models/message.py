import datetime as _dt
from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base

class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, index=True)
    # Foreign Key thread_id
    thread_id = Column(Integer, ForeignKey("thread.id"), index=True)
    is_bot = Column(Boolean, default=False)
    is_user = Column(Boolean, default=False)
    message = Column(String, index=True)
    created_at = Column(DateTime, default=_dt.datetime.now())
    updated_at = Column(DateTime, default=_dt.datetime.now())

    thread = relationship("Thread", back_populates="message")