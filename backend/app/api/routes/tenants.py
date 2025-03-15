from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.services.tenant_service import create_new_tenant
from backend.app.auth.services import require_super_admin
from pydantic import BaseModel

router = APIRouter()

# Define request body schema
class TenantCreateRequest(BaseModel):
    name: str
    description: str

@router.post("/tenants/")
def create_tenant(
    request: TenantCreateRequest, 
    db: Session = Depends(get_db),
    super_admin = Depends(require_super_admin)  # Restrict access
):
    tenant = create_new_tenant(db, request)
    return {"message": "Tenant created successfully", "tenant": tenant}
