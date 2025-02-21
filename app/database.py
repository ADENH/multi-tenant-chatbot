from sqlalchemy import create_engine
from pymongo import MongoClient
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from app.models import Base
import os

load_dotenv()  # Load environment variables from .env file

print(os.getenv("DATABASE_URL"))
DATABASE_URL = os.getenv("DATABASE_URL")
MONGO_URI = os.getenv("MONGO_URI")

# PostgreSQL Connection
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Create all tables defined in the models
Base.metadata.create_all(bind=engine)

# MongoDB Connection
mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client["chat_history"]

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db  # Provide the session to the route handler
    finally:
        db.close()  # Ensure the session is closed after use
