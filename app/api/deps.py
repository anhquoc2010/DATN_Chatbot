from fastapi import Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings

from app.core.database import SessionLocal


async def get_session():
    async with SessionLocal() as session:
        yield session
