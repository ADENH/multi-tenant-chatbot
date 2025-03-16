from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.auth.services import register_user, authenticate_user
from backend.app.schemas import UserCreate, Token, LoginRequest
from backend.app.database import SessionLocal

router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user)

@router.post("/login", response_model=Token )
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    return authenticate_user(db, login_data)

@router.post("/add-user", response_model=UserCreate)
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    return add_user(db, user)
