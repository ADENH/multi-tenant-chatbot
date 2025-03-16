from sqlalchemy.orm import Session
from backend.app.models.models import User, Tenant
from backend.app.auth.security import hash_password, verify_password, create_access_token
from backend.app.schemas import UserCreate, LoginRequest, Token
from fastapi import HTTPException, status, Depends, Header
from fastapi.security import OAuth2PasswordBearer
from backend.app.database import get_db
from backend.app.config import settings
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Secret key & algorithm
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"

def register_user(db: Session, user: UserCreate):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(user.password)
    new_user = User(email=user.email, password_hash=hashed_password,username=user.username , tenant_id=user.tenant_id, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token({"sub": new_user.email, "tenant_id": new_user.tenant_id, "role": new_user.role})
    return {"access_token": access_token, "token_type": "bearer"}

def authenticate_user(db: Session, login_data: LoginRequest):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": user.email, "tenant_id": user.tenant_id, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

def add_user(db: Session, user: UserCreate):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    if user.role == "super_admin":
        # not save tenant_id for super_admin
        new_user = User(email=user.email, password_hash=hashed_password, role=user.role)
    else:
        # tenant_admin or user
        new_user = User(email=user.email, password_hash=hashed_password, tenant_id=user.tenant_id, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token({"sub": new_user.email, "tenant_id": new_user.tenant_id, "role": new_user.role})
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Extract user from token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

def require_super_admin(user: User = Depends(get_current_user)):
    """Only allows Super Admins"""
    if user.role != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Super Admins can create tenants",
        )
    return user
    

def get_current_tenant(x_tenant_id: str = Header(None), db: Session = Depends(get_db)):
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="Tenant ID is required in X-Tenant-ID header")
    tenant = db.query(Tenant).filter(Tenant.id == x_tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant

def get_current_super_admin(db: Session = Depends(get_db), x_tenant_id: str = Header(None)):
    # Ensure user is a super admin
    user = db.query(User).filter(User.tenant_id == x_tenant_id, User.role == "super_admin").first()
    if not user:
        raise HTTPException(status_code=403, detail="Only super admins can perform this action")
    return user

