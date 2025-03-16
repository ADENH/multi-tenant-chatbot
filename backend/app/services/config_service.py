import uuid
from sqlalchemy.orm import Session
from backend.app.models.models import Config
from backend.app.schemas import ConfigCreateRequest

def create_config(db: Session, tenant_id: str, request: ConfigCreateRequest):
    config_id = str(uuid.uuid4())
    config = Config(config_id=config_id, tenant_id=tenant_id, key=request.key, value=request.value)
    db.add(config)
    db.commit()
    db.refresh(config)
    return config

def get_config(db: Session, tenant_id: str, key: str):
    return db.query(Config).filter(Config.tenant_id == tenant_id, Config.key == key).first()
