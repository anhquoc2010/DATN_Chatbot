from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.campaigns import Campaign  # Ensure this is a Pydantic model
from app.api.deps import get_session
from app.services.crud.campaigns import crud_campaign
from app.schemas.campaigns import CampaignCreate, CampaignUpdate, CampaignOut
import datetime as _dt

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])

@router.get("/", response_model=List[CampaignOut])
async def get_all_campaigns(
    session: AsyncSession = Depends(get_session)
):
    campaigns = await crud_campaign.get_multi(session)
    if not campaigns:
        raise HTTPException(status_code=404, detail="Campaigns not found")
    else:
        # sort by created_at, oldest first
        campaigns = sorted(campaigns, key=lambda x: x.created_at)
    return campaigns