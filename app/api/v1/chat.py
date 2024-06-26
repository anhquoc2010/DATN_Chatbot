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
print(os.environ.get("OPENAI_API_KEY"))
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
    user_id: int,
    session: AsyncSession = Depends(get_session)
):
    # Step 1: Generate a response using GPT-3.5
    response_content = generate_response(question)
    # check if response is ''
    if response_content == '':
        raise HTTPException(status_code=400, detail="Error generating response")
    else:
        filters = {
            "organization_id": organization_id,
            "user_id": user_id,
        }
        try:
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
            user_message = {
                "message": question,
                "thread_id": thread.id,
                "is_user": True,
                "is_bot": False,
            }
            await crud_message.create(session, MessageCreate(**user_message))

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
