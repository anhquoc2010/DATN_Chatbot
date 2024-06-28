import asyncio
import json
import logging
from app.models.base import Base  # Import the Base class correctly
from app.core import database
from app.models import *  # Import all models
from app.core.config import settings
import datetime as dt

from app.services.crud.thread import crud_thread
from app.services.crud.message import crud_message
from app.models.thread import Thread
from app.models.message import Message
from app.schemas.thread import ThreadCreate, ThreadUpdate
from app.schemas.message import MessageCreate, MessageUpdate
# Configure logging

# Enable SQLAlchemy logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

async def _add_tables():
    try:
        async with database.get_async_engine().begin() as conn:
            # Drop and create specific tables
            try:
                await conn.run_sync(Thread.__table__.drop)
                await conn.run_sync(Message.__table__.drop)
            except Exception as e:
                print("Error:", e)
                pass

            try:
                await conn.run_sync(Thread.__table__.create)
                await conn.run_sync(Message.__table__.create)
            except Exception as e:
                print("Error:", e)
                pass
    except Exception as e:
        print("Error:", e)
        pass
asyncio.run(_add_tables())

threads_data = [
    {
        "title": "Thread 1",
        "description": "Description 1",
        "organization_id": 1,
        "user_id": 1,
        "created_at": dt.datetime.now(),
        "updated_at": dt.datetime.now(),
    },
    {
        "title": "Thread 2",
        "description": "Description 2",
        "organization_id": 2,
        "user_id": 2,
        "created_at": dt.datetime.now(),
        "updated_at": dt.datetime.now(),
    },
    {
        "title": "Thread 3",
        "description": "Description 3",
        "organization_id": 3,
        "user_id": 3,
        "created_at": dt.datetime.now(),
        "updated_at": dt.datetime.now(),
    },
    {
        "title": "Thread 4",
        "description": "Description 4",
        "organization_id": 4,
        "user_id": 4,
        "created_at": dt.datetime.now(),
        "updated_at": dt.datetime.now(),
    },
    {
        "title": "Thread 5",
        "description": "Description 5",
        "organization_id": 5,
        "user_id": 5,
        "created_at": dt.datetime.now(),
        "updated_at": dt.datetime.now(),
    }
]

messages_data = [
    {
        "thread_id": 1,
        "is_bot": False,
        "is_user": True,
        "message": "Message 1",
        "created_at": dt.datetime.now(),
        "updated_at": dt.datetime.now(),
    },
    {
        "thread_id": 2,
        "is_bot": False,
        "is_user": True,
        "message": "Message 2",
        "created_at": dt.datetime.now(),
        "updated_at": dt.datetime.now(),
    },
    {
        "thread_id": 3,
        "is_bot": False,
        "is_user": True,
        "message": "Message 3",
        "created_at": dt.datetime.now(),
        "updated_at": dt.datetime.now(),
    },
    {
        "thread_id": 4,
        "is_bot": False,
        "is_user": True,
        "message": "Message 4",
        "created_at": dt.datetime.now(),
        "updated_at": dt.datetime.now(),
    }
]


async def insert_data():
    try:
        session = database.SessionLocal()
        
        for thread in threads_data:
            thread_in = ThreadCreate(**thread)
            await crud_thread.create(session, thread_in)
        await session.commit()
        for message in messages_data:
            message_in = MessageCreate(**message)
            await crud_message.create(session, message_in)
    except Exception as e:
        print("Error:", e)
    finally:
        await session.commit()
        await session.close()
        
# Run the coroutine
# asyncio.run(insert_data())
