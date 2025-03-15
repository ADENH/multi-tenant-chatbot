from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.services.tenant_service import create_new_tenant
from backend.app.auth.services import require_super_admin

router = APIRouter()

@router.post("/tenants/")
def create_tenant(
    name: str, 
    description: str, 
    db: Session = Depends(get_db),
    super_admin = Depends(require_super_admin)  # Restrict access
):
    tenant = create_new_tenant(db, name, description)
    return {"message": "Tenant created successfully", "tenant": tenant}
