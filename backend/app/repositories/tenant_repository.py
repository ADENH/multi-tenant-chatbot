from sqlalchemy.orm import Session
from backend.app.models.models import Tenant
import uuid

def create_tenant(db: Session, name: str, description: str):
    tenant = Tenant(id=str(uuid.uuid4()), name=name, description=description)
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant
