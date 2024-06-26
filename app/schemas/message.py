# import datetime as _dt
# from sqlalchemy import Boolean, Column, Integer, String, DateTime
# from sqlalchemy.orm import relationship

# from app.models.base import Base

# class Messages(Base):
#     __tablename__ = "message"

#     id = Column(Integer, primary_key=True, index=True)
#     thread_id = Column(Integer, index=True)
#     is_bot = Column(Boolean, default=False)
#     is_user = Column(Boolean, default=False)
#     message = Column(String, index=True)
#     created_at = Column(DateTime, default=_dt.datetime.now())
#     updated_at = Column(DateTime, default=_dt.datetime.now())

#     thread = relationship("Threads", back_populates="message")

from typing import Optional

from pydantic import BaseModel

class MessageBase(BaseModel):
    thread_id: Optional[int]
    is_bot: Optional[bool]
    is_user: Optional[bool]
    message: Optional[str]

class MessageCreate(MessageBase):
    pass

class MessageUpdate(MessageBase):
    pass

class MessageOut(MessageBase):
    id: int

    class Config:
        from_attributes = True

class MessageInDB(MessageBase):
    pass