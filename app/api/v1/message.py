from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.message import Message  # Ensure this is a Pydantic model
from app.api.deps import get_session
from app.services.crud.message import crud_message
from app.schemas.message import MessageCreate, MessageUpdate, MessageOut
import datetime as _dt
router = APIRouter(prefix="/message", tags=["Message"])

@router.get("/", response_model=List[MessageOut])
async def get_all_messages(
    session: AsyncSession = Depends(get_session)
):
    messages = await crud_message.get_multi(session)
    if not messages:
        raise HTTPException(status_code=404, detail="Messages not found")
    else:
        # sort by created_at, oldest first
        messages = sorted(messages, key=lambda x: x.created_at)
    return messages

@router.post("/", response_model=MessageOut)
async def create_message(
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    data = await request.json()
    message = await crud_message.create(session, obj_in=data)
    return message

@router.get("/{message_id}", response_model=MessageOut)
async def get_message_by_id(
    message_id: int,
    session: AsyncSession = Depends(get_session)
):
    message = await crud_message.get(session, id=message_id)
    return message

@router.get("/thread/{thread_id}", response_model=List[MessageOut])
async def get_messages_by_thread_id(
    thread_id: int,
    session: AsyncSession = Depends(get_session)
):
    messages = await crud_message.get_multi(session, thread_id=thread_id)
    if not messages:
        raise HTTPException(status_code=404, detail="Messages not found")
    else:
        # sort by created_at, oldest first
        messages = sorted(messages, key=lambda x: x.created_at)
    return messages

@router.put("/{message_id}", response_model=MessageOut)
async def update_message(
    message_id: int,
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    data = await request.json()
    message = await crud_message.update(session, id=message_id, obj_in=data)
    return message

@router.delete("/{message_id}", response_model=MessageOut)
async def delete_message(
    message_id: int,
    session: AsyncSession = Depends(get_session)
):
    message = await crud_message.remove(session, id=message_id)
    return message

@router.get("/search/", response_model=List[MessageOut])
async def search_messages(
    request: Request,
    session: AsyncSession = Depends(get_session),
    offset: int = Query(0, ge=0),
    limit: int = Query(100, le=100)
):
    filters = {key: value for key, value in request.query_params.items() if key not in ['offset', 'limit']}
    messages = await crud_message.search(session, offset=offset, limit=limit, **filters)
    if not messages:
        return []
    else:
        # sort by created_at, oldest first
        messages = sorted(messages, key=lambda x: x.created_at)
    return messages