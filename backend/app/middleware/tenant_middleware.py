from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

class TenantMiddleware(BaseHTTPMiddleware):
    """Middleware to extract tenant ID from headers"""

    def __init__(self, app):
        super().__init__(app)
        self.exclude_paths = ["/api/v1/tenants/", "/auth/"]  # Exclude tenant creation API and authentication

    async def dispatch(self, request: Request, call_next):
        """Process request to enforce tenant ID"""

        # Skip validation for excluded paths
        if any(request.url.path.startswith(path) for path in self.exclude_paths):
            return await call_next(request)

        # Check for X-Tenant-ID header
        tenant_id = request.headers.get("X-Tenant-ID")
        if not tenant_id:
            raise HTTPException(status_code=400, detail="Tenant ID is required in X-Tenant-ID header")

        # Pass tenant ID in request state
        request.state.tenant_id = tenant_id

        response = await call_next(request)
        return response
