from app.services.crud.base import CRUDBase
from app.models.campaigns import Campaign
from app.schemas.campaigns import CampaignCreate, CampaignUpdate

CRUDCampaign = CRUDBase[Campaign, CampaignCreate, CampaignUpdate]
crud_campaign = CRUDCampaign(Campaign)