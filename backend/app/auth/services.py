from sqlalchemy.orm import Session
from backend.app.models.models import User
from backend.app.auth.security import hash_password, verify_password, create_access_token
from backend.app.schemas import UserCreate, LoginRequest, Token
from fastapi import HTTPException, status

def register_user(db: Session, user: UserCreate):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password, tenant_id=user.tenant_id, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token({"sub": new_user.email, "tenant_id": new_user.tenant_id, "role": new_user.role})
    return {"access_token": access_token, "token_type": "bearer"}

def authenticate_user(db: Session, login_data: LoginRequest):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": user.email, "tenant_id": user.tenant_id, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}
