from app.database import SessionLocal
from app.models import User
from app.auth import hash_password

def create_service_user(username: str, password: str, tenant_id: str = None):
    db = SessionLocal()
    try:
        # Check if the user already exists
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            print(f"User '{username}' already exists.")
            return

        # Create a new user
        hashed_password = hash_password(password)
        new_user = User(
            username=username,
            hashed_password=hashed_password,
            tenant_id=tenant_id
        )
        db.add(new_user)
        db.commit()
        print(f"Service user '{username}' created successfully.")
    finally:
        db.close()

if __name__ == "__main__":
    create_service_user(username="admin", password="admin123", tenant_id="tenant_1")