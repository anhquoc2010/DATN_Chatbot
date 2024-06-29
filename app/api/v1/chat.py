from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_session
from app.schemas.message import MessageCreate, MessageUpdate, MessageOut
from app.schemas.thread import ThreadCreate, ThreadUpdate, ThreadOut
from app.services.crud.message import crud_message
from app.services.crud.thread import crud_thread
from app.services.crud.organizations import crud_organization
from app.services.crud.campaigns import crud_campaign
from app.schemas.organizations import OrganizationCreate, OrganizationUpdate, OrganizationOut
from app.schemas.campaigns import CampaignCreate, CampaignUpdate, CampaignOut
from openai import OpenAI
import os
import datetime as dt

# Make sure to set your OpenAI API key as an environment variable
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

router = APIRouter(prefix="/chat", tags=["Chat"])

async def generate_response(question: str, organization_id: int, thread_id: int, session: AsyncSession):
    prompt_template = """
    Bạn là một trợ lý AI xuất sắc, bạn sẽ trả lời các câu hỏi của tôi về các tổ chức và chiến dịch dựa trên dữ liệu và lịch sử tin nhắn. Hãy trả lời thật ngắn gọn và rõ ràng nhé!

    Dữ liệu tổ chức và chiến dịch thuộc tổ chức đó:
    {organization_data}

    Lịch sử tin nhắn:
    {message_data}

    Câu hỏi: {question}

    Câu trả lời:
    """
    filters = {
        "id": organization_id
    }
    organization = await crud_organization.search(session, offset=0, limit=1, **filters)
    campaigns = await crud_campaign.get_multi(session)
    
    # return organizations, each with a list of campaigns
    orgs = []
    for org in organization:
        org_dict = org.dict()
        org_dict['campaigns'] = []
        for campaign in campaigns:
            if campaign.organization_id == org.id:
                campaign_dict = campaign.dict()
                campaign_dict['created_at'] = campaign.created_at.isoformat() if campaign.created_at else None
                campaign_dict['updated_at'] = campaign.updated_at.isoformat() if campaign.updated_at else None
                org_dict['campaigns'].append(campaign_dict)
        orgs.append(org_dict)
    org = orgs[0]
    organization_data = str(org).replace("'", '')

    filter = {'thread_id': thread_id}
    messages = await crud_message.search(session, offset=0, limit=100, **filter)
    if messages:
        # sort by id
        messages = sorted(messages, key=lambda x: x.id)
    # convert messages to dictionary
    messages = [message.dict() for message in messages]
    message_data = str(messages).replace("'", '')
    prompt = prompt_template.format(
        organization_data=organization_data,
        message_data=message_data,
        question=question
    )
    print("Prompt:", prompt)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                 {
                    "role": "user",
                    "content": [
                        {
                        "type": "text",
                        "text": prompt
                        }
                    ]
                }
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
            response_content = await generate_response(question, organization_id, thread.id, session)
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
