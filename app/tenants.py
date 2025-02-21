from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import engine
from app.models import Tenant
from pydantic import BaseModel
from app.database import get_db
import uuid

router = APIRouter()

class TenantCreate(BaseModel):
    name: str

@router.post("/register")
def register_tenant(tenant_data: TenantCreate, db: Session = Depends(get_db)):
    """
    Register a new tenant with a unique API key.
    Expects JSON payload: {"name": "TenantName"}
    """
    # Generate a unique API key
    api_key = str(uuid.uuid4())

    # Create a new Tenant instance
    new_tenant = Tenant(name=tenant_data.name, api_key=api_key)

    try:
        # Add and commit the new tenant to the database
        db.add(new_tenant)
        db.commit()
        db.refresh(new_tenant)  # Refresh to get any auto-generated fields
    except Exception as e:
        # Rollback in case of error
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return {"name": tenant_data.name, "api_key": api_key}
