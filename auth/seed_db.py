import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from database.db_connection import engine, SessionLocal
from auth.models import User
from auth.security import get_password_hash
from auth.database import Base


def seed_database():
    print("[INFO] Initializing database tables...")
    # Create the tables
    Base.metadata.create_all(bind=engine)
    print("[SUCCESS] Tables initialized.")

    db = SessionLocal()
    try:
        # Check if users already exist
        existing_users = db.query(User).count()
        if existing_users > 0:
            print("[INFO] Users table already contains data. Seeding skipped.")
            return

        print("[INFO] Seeding default users...")
        default_users = [
            User(
                username="admin",
                email="admin@sportavista.pro",
                password_hash=get_password_hash("admin123"),
                role="admin",
            ),
            User(
                username="coach",
                email="coach@sportavista.pro",
                password_hash=get_password_hash("coach123"),
                role="coach",
            ),
            User(
                username="scout",
                email="scout@sportavista.pro",
                password_hash=get_password_hash("scout123"),
                role="scout",
            ),
            User(
                username="analyst",
                email="analyst@sportavista.pro",
                password_hash=get_password_hash("analyst123"),
                role="analyst",
            ),
        ]

        db.add_all(default_users)
        db.commit()
        print("[SUCCESS] Database seeding completed successfully!")
        print("Default accounts created:")
        for u in default_users:
            print(f"  - Username: {u.username} | Role: {u.role}")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error seeding database: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
