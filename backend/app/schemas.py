from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
    tenant_id: int
    role: str

class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
