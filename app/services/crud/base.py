from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from sqlalchemy import select, func, JSON, DateTime
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from fastapi.responses import JSONResponse
import json
from sqlalchemy.exc import SQLAlchemyError
from app.services.utils import to_dict

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self._model = model

    async def create(
        self, session: AsyncSession, obj_in: CreateSchemaType
    ) -> ModelType:
        try:
            obj_in_data = dict(obj_in)
            db_obj = self._model(**obj_in_data)
            session.add(db_obj)
            await session.commit()
            return db_obj
        except Exception as e:
            print(e)
            return None

    async def get(self, session: AsyncSession, *args, **kwargs) -> Optional[ModelType]:
        try:
            result = await session.execute(
            select(self._model).filter(*args).filter_by(**kwargs)
            )
            return result.scalars().first()
        except Exception as e:
            print(e)
            return None

    async def get_multi(
        self, session: AsyncSession, *args, offset: int = 0, limit: int = 100, **kwargs
    ) -> List[ModelType]:
        try:
            result = await session.execute(
                select(self._model)
                .filter(*args)
                .filter_by(**kwargs)
                .offset(offset)
                .limit(limit)
            )
            return result.scalars().all()
        except Exception as e:
            print(e)
            return []


    async def update(
        self,
        session: AsyncSession,
        *,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
        db_obj: Optional[ModelType] = None,
        **kwargs
    ) -> Optional[ModelType]:
        db_obj = db_obj or await self.get(session, **kwargs)
        if not db_obj:
            return None

        obj_data = db_obj.dict()
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)
        
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        
        session.add(db_obj)
        try:
            await session.commit()
            await session.refresh(db_obj)
        except Exception as e:
            await session.rollback()
            raise e
        
        return db_obj


    async def delete(
        self, session: AsyncSession, *args, db_obj: Optional[ModelType] = None, **kwargs
    ) -> ModelType:
        db_obj = db_obj or await self.get(session, *args, **kwargs)
        await session.delete(db_obj)
        await session.commit()
        return db_obj


    async def search(
            self, session: AsyncSession, offset: int = 0, limit: int = 100, **kwargs
        ) -> List[Any]:
            try:
                query = select(self._model)
                
                for key, value in kwargs.items():
                    column_attr = getattr(self._model, key, None)
                    if column_attr is not None:
                        if column_attr.type.python_type == int:
                            query = query.filter(column_attr == int(value))
                        elif column_attr.type.python_type == str:
                            query = query.filter(column_attr.ilike(f"%{value}%"))
                        elif column_attr.type.python_type == datetime:
                            query = query.filter(column_attr == datetime.fromisoformat(value))
                        else:
                            query = query.filter(column_attr == value)
                result = await session.execute(query)
                result = result.scalars().all()
                total_records = len(result)
                query = query.offset(offset).limit(total_records)
                
                result = await session.execute(query)
                return result.scalars().all()
            except Exception as e:
                print(e)
                return []