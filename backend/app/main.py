from fastapi import FastAPI
from backend.app.auth.routes import router as auth_router
from backend.app.api.routes.tenants import router as tenant
from backend.app.middleware.tenant_middleware import TenantMiddleware

app = FastAPI(title="Multi-Tenant AI Chatbot")

# Include routes
app.include_router(auth_router)
app.include_router(tenant, prefix="/api/v1", tags=["Tenant Management"])

app.add_middleware(TenantMiddleware)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Multi-Tenant AI Chatbot API"}
