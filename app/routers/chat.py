from fastapi import APIRouter, Depends, HTTPException,FastAPI, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models import User
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.ai_logic import chat_with_openai

app = FastAPI()
router = APIRouter()

# Initialize the rate limiter
limiter = Limiter(key_func=get_remote_address)

@router.post("/")
@limiter.limit("5/minute")  # Allow 5 requests per minute
def chat(
    request: Request,  # Add the request parameter
    message: str,
    current_user: User = Depends(get_current_user),
):
    """
    Handle chat requests and generate AI responses.
    """
    # Access tenant_id directly from the User object
    tenant_id = current_user.tenant_id
    if not tenant_id:
        raise HTTPException(status_code=400, detail="Tenant ID not found for the user")
    # Call the AI logic to generate a response
    response = chat_with_openai(tenant_id, message)
    
    return {"response": response}