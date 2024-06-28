from app.services.crud.base import CRUDBase
from app.models.organizations import Organization
from app.schemas.organizations import OrganizationCreate, OrganizationUpdate

CRUDOrganization = CRUDBase[Organization, OrganizationCreate, OrganizationUpdate]
crud_organization = CRUDOrganization(Organization)