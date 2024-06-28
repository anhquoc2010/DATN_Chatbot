from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_session
from app.schemas.message import MessageCreate, MessageUpdate, MessageOut
from app.schemas.thread import ThreadCreate, ThreadUpdate, ThreadOut
from app.services.crud.message import crud_message
from app.services.crud.thread import crud_thread
from openai import OpenAI
import os
import datetime as dt

# Make sure to set your OpenAI API key as an environment variable
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

router = APIRouter(prefix="/chat", tags=["Chat"])

def generate_response(question: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
                {"role": "user", "content": question},
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Error:", e)
        return ''



# RAG chatbot
@router.post("/", response_model=MessageOut)
async def chat(
    question: str,
    organization_id: int,
    user_id: int = 1,
    is_user: bool = True,
    session: AsyncSession = Depends(get_session)
):
    filters = {
        "organization_id": organization_id,
        "user_id": user_id,
    }
    threads = await crud_thread.search(session, offset=0, limit=1, **filters)
    if not threads:
        thread_data = {
            "title": "Thread",
            "description": "Description",
            "organization_id": organization_id,
            "user_id": user_id,
            "created_at": dt.datetime.now(),
            "updated_at": dt.datetime.now(),
        }
        thread = await crud_thread.create(session, ThreadCreate(**thread_data))
    else:
        thread = threads[0]
    if is_user:
        user_message = {
            "message": question,
            "thread_id": thread.id,
            "is_user": True,
            "is_bot": False,
        }
    else:
        user_message = {
            "message": question,
            "thread_id": thread.id,
            "is_user": False,
            "is_bot": False,
        }

    result = await crud_message.create(session, MessageCreate(**user_message))
    # Step 1: Generate a response using GPT-3.5
    if is_user:
        try:
            response_content = generate_response(question)
        except Exception as e:
            print("Error:", e)
            response_content = ''
        # check if response is ''
        if response_content == '':
            print("No response from Generative AI")
            response_content = "Xin lỗi, tôi không hiểu câu hỏi của bạn. Bạn có thể đặt câu hỏi khác không?"
        try:
            bot_message = {
                "message": response_content,
                "thread_id": thread.id,
                "is_user": False,
                "is_bot": True,
            }
            result = await crud_message.create(session, MessageCreate(**bot_message))
            return result
        except Exception as e:
            print("Error:", e)

    return result
