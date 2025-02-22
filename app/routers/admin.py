from fastapi import APIRouter, Depends
from app.auth import require_role, require_permission, require_tenant_access

router = APIRouter()

@router.get("/tenants")
def list_all_tenants(current_user=Depends(require_role("super_admin"))):
    """
    Super admin-only endpoint to list all tenants.
    """
    return {"message": "This is a super admin-only endpoint."}

@router.get("/tenants/{tenant_id}/users")
def list_tenant_users(
    tenant_id: str,
    current_user=Depends(require_tenant_access),
):
    """
    Admin-only endpoint to list users of a specific tenant.
    """
    return {"message": f"Users of tenant {tenant_id} listed successfully."}

@router.post("/chat")
def send_message(current_user=Depends(require_permission("send_messages"))):
    """
    Endpoint accessible to users with the 'send_messages' permission.
    """
    return {"message": "Message sent successfully."}

@router.get("/public-info")
def view_public_info(current_user=Depends(require_permission("view_public_info"))):
    """
    Public information accessible to all roles (including guests).
    """
    return {"message": "This is public information."}