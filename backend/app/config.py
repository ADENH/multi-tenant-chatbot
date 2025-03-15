import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost/chatbot_db")
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Settings(BaseSettings):
    PROJECT_NAME: str = "Multi-Tenant AI Chatbot"
    SECRET_KEY: str =  os.getenv("SECRET_KEY", "your_secret_key")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost/chatbot_db")

    class Config:
        case_sensitive = True

# Create an instance of Settings
settings = Settings()
