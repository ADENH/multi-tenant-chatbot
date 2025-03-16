from sqlalchemy.orm import Session
from backend.app.models.models import Tenant
import uuid
from backend.app.schemas import TenantCreateRequest

def create_tenant(db: Session, request: TenantCreateRequest):
    name = request.name
    description = request.description
    tenant = Tenant(id=str(uuid.uuid4()), name=name, description=description)
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant
