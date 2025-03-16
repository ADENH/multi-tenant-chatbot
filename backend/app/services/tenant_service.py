from sqlalchemy.orm import Session
from backend.app.repositories.tenant_repository import create_tenant
from backend.app.schemas import TenantCreateRequest

def create_new_tenant(db: Session, request: TenantCreateRequest):
    return create_tenant(db, request)
