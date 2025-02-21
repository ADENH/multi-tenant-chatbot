from fastapi import FastAPI, Depends, HTTPException, APIRouter
from app.chatbot import chat_with_ai
from app.auth import decode_token,create_access_token, get_password_hash, verify_password, get_current_user
from app.tenants import router as tenant_router
from app.routers import auth, chat
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from pydantic import BaseModel

app = FastAPI()
router = APIRouter()
app.include_router(tenant_router, prefix="/tenants")
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str

# @app.post("/chat")
# def chat(request: ChatRequest, current_user: dict = Depends(get_current_user)):
#     print('token', current_user)
#     # Extract tenant_id from the current_user dictionary
#     tenant_id = current_user.get("tenant_id")
#     print('tenant_id', tenant_id)
#     if not tenant_id:
#         raise HTTPException(status_code=400, detail="Tenant ID not found in token")

#     response = chat_with_ai(tenant_id, message)
#     return {"response": response}

# Fake user database (replace with real database)
fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Admin User",
        "tenant_id": "TenantABC",
        "email": "admin@example.com",
        "hashed_password": get_password_hash("password123"),
    }
}


# @app.post("/token")
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = fake_users_db.get(form_data.username)
#     if not user or not verify_password(form_data.password, user["hashed_password"]):
#         raise HTTPException(status_code=400, detail="Invalid username or password")
    
#     access_token = create_access_token({"sub": user["username"]}, expires_delta=timedelta(minutes=30))
#     return {"access_token": access_token, "token_type": "bearer"}


@app.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello, {current_user['sub']}! You have access to this protected route."}
