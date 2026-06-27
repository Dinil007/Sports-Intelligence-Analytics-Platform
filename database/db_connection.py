import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# --------------------------------------------------
# Load .env file from project root
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

# --------------------------------------------------
# Read database configuration
# --------------------------------------------------
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# --------------------------------------------------
# Build PostgreSQL connection URL
# --------------------------------------------------
DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# --------------------------------------------------
# Create SQLAlchemy Engine
# --------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False,  # Set to True if you want SQL queries printed
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
)

# --------------------------------------------------
# Create Session Factory
# --------------------------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# --------------------------------------------------
# Dependency / Session Generator
# --------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------------------------------------------------
# Connection Test Function
# --------------------------------------------------
def test_connection():
    try:
        with engine.connect() as conn:
            version = conn.execute(text("SELECT version();")).scalar()
            print("✅ PostgreSQL Connected Successfully!")
            print(version)
    except Exception as e:
        print("❌ Database Connection Failed!")
        print(e)

# --------------------------------------------------
# Run only if executed directly
# --------------------------------------------------
if __name__ == "__main__":
    test_connection()