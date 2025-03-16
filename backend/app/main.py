from fastapi import FastAPI
from backend.app.auth.routes import router as auth_router
from backend.app.api.routes import tenants, configs

from backend.app.middleware.tenant_middleware import TenantMiddleware

app = FastAPI(title="Multi-Tenant AI Chatbot")

# Include routes
app.include_router(auth_router)
app.include_router(tenants.router, prefix="/api/v1", tags=["Tenant Management"])
app.include_router(configs.router, prefix="/configs", tags=["Configs"])

app.add_middleware(TenantMiddleware)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Multi-Tenant AI Chatbot API"}
