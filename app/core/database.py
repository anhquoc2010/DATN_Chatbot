from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

def get_async_engine():
    return create_async_engine(settings.POSTGRES_URI, echo = True)

def get_async_session():
    engine = get_async_engine()
    return sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

engine = create_async_engine(settings.POSTGRES_URI)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
