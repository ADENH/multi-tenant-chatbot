from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: str
    username: str
    password: str
    role: str = Field(..., pattern="^(super_admin|admin|user)$")
    tenant_id: Optional[str] = None  # <-- Make tenant_id optional

    @classmethod
    def validate_tenant(cls, values):
        if values["role"] != "super_admin" and not values.get("tenant_id"):
            raise ValueError("tenant_id is required for admin and user roles")
        return values
class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TenantCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None

class TenantResponse(BaseModel):
    tenant_id: str
    name: str
    description: Optional[str]

class ConfigCreateRequest(BaseModel):
    key: str
    value: str

class ConfigResponse(BaseModel):
    config_id: str
    tenant_id: str
    key: str
    value: str

