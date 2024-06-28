from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.organizations import Organization  # Ensure this is a Pydantic model
from app.api.deps import get_session
from app.services.crud.organizations import crud_organization
from app.schemas.organizations import OrganizationCreate, OrganizationUpdate, OrganizationOut
import datetime as _dt

router = APIRouter(prefix="/organizations", tags=["Organizations"])

@router.get("/", response_model=List[OrganizationOut])
async def get_all_organizations(
    session: AsyncSession = Depends(get_session)
):
    organizations = await crud_organization.get_multi(session)
    if not organizations:
        raise HTTPException(status_code=404, detail="Organizations not found")
    else:
        # sort by created_at, oldest first
        organizations = sorted(organizations, key=lambda x: x.created_at)
    return organizations
