from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.organizations import Organization  # Ensure this is a Pydantic model
from app.models.campaigns import Campaign
from app.api.deps import get_session
from app.services.crud.organizations import crud_organization
from app.services.crud.campaigns import crud_campaign
from app.schemas.organizations import OrganizationCreate, OrganizationUpdate, OrganizationOut
from app.schemas.campaigns import CampaignCreate, CampaignUpdate, CampaignOut
import datetime as _dt
import json
import datetime  # Add this import

router = APIRouter(prefix="/rag", tags=["RAG"])

@router.get("/re_embedding")
async def re_embedding(
    session: AsyncSession = Depends(get_session)
):
    organizations = await crud_organization.get_multi(session)
    campaigns = await crud_campaign.get_multi(session)
    
    # return organizations, each with a list of campaigns
    orgs = []
    for org in organizations:
        org_dict = org.dict()
        org_dict['campaigns'] = []
        for campaign in campaigns:
            if campaign.organization_id == org.id:
                campaign_dict = campaign.dict()
                campaign_dict['created_at'] = campaign.created_at.isoformat() if campaign.created_at else None
                campaign_dict['updated_at'] = campaign.updated_at.isoformat() if campaign.updated_at else None
                org_dict['campaigns'].append(campaign_dict)
        orgs.append(org_dict)
    text_data = str(orgs)
    return 
