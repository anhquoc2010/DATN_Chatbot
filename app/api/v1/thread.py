from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update, delete, insert, and_, or_, func, desc, asc, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from fastapi import Query
from fastapi import Request
from app.models.thread import Thread
from app.schemas.thread import ThreadCreate, ThreadUpdate, ThreadOut
from app.services.crud.message import crud_message
from app.schemas.message import MessageCreate, MessageUpdate, MessageOut
from app.api.deps import (
    get_session
)
from app.services.crud.thread import crud_thread

router = APIRouter(prefix="/thread", tags=["Thread"])

@router.get("/", response_model=List[ThreadOut])
async def get_all_threads(
    session: AsyncSession = Depends(get_session)
):
    threads = await crud_thread.get_multi(session)
    return threads

@router.post("/", response_model=ThreadOut)
async def create_thread(
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    data = await request.json()
    thread = await crud_thread.create(session, obj_in=data)
    return thread

@router.get("/{thread_id}", response_model=ThreadOut)
async def get_thread_by_id(
    thread_id: int,
    session: AsyncSession = Depends(get_session)
):
    thread = await crud_thread.get(session, id=thread_id)
    return thread

@router.put("/{thread_id}", response_model=ThreadOut)
async def update_thread(
    thread_id: int,
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    data = await request.json()
    thread = await crud_thread.update(session, id=thread_id, obj_in=data)
    return thread

@router.delete("/{thread_id}", response_model=ThreadOut)
async def delete_thread(
    thread_id: int,
    session: AsyncSession = Depends(get_session)
):
    thread = await crud_thread.remove(session, id=thread_id)
    return thread

@router.get("/search/")
async def search_threads(
    request: Request,
    session: AsyncSession = Depends(get_session),
    offset: int = Query(0, ge=0),
    limit: int = Query(100, le=100)
):
    filters = {key: value for key, value in request.query_params.items() if key not in ['offset', 'limit']}
    threads = await crud_thread.search(session, offset=offset, limit=limit, **filters)
    if not threads:
        return []
    else:
        # sort by created_at, oldest first
        threads = sorted(threads, key=lambda x: x.created_at)
        latest_threads = []
        for thread in threads:
            filter = {'thread_id': thread.id}
            messages = await crud_message.search(session, offset=0, limit=100, **filter)
            if messages:
                # sort by id
                messages = sorted(messages, key=lambda x: x.id, reverse=True)
                # add messages to thread(thread has no messages attribute), add messages attribute to thread
                thread.messages = messages
                latest_threads.append(thread)
                print(thread.messages)
    return latest_threads
