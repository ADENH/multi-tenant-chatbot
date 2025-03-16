from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.services.config_service import create_config, get_config
from backend.app.schemas import ConfigCreateRequest, ConfigResponse
from backend.app.auth.services import get_current_tenant  # Middleware for tenant auth

router = APIRouter()

@router.post("/", response_model=ConfigResponse)
def set_config(request: ConfigCreateRequest, db: Session = Depends(get_db), tenant=Depends(get_current_tenant)):
    return create_config(db, tenant.id, request)

@router.get("/{key}", response_model=ConfigResponse)
def get_config_value(key: str, db: Session = Depends(get_db), tenant=Depends(get_current_tenant)):
    config = get_config(db, tenant.id, key)
    if not config:
        raise HTTPException(status_code=404, detail="Config not found")
    return config
