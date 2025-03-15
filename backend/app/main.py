from fastapi import FastAPI
from backend.app.auth.routes import router as auth_router

app = FastAPI(title="Multi-Tenant AI Chatbot")

# Include routes
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Multi-Tenant AI Chatbot API"}
