from sqlalchemy.orm import Session
from backend.app.repositories.tenant_repository import create_tenant

def create_new_tenant(db: Session, name: str, description: str):
    return create_tenant(db, name, description)
