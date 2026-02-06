from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Get the appropriate database URL
database_url = settings.get_database_url()

# Configure connection arguments based on database type
connect_args = {}
if settings.is_sqlite:
    connect_args = {"check_same_thread": False}
elif settings.is_mysql:
    connect_args = {
        "charset": "utf8mb4",
        "connect_timeout": 60,
        "read_timeout": 30,
        "write_timeout": 30,
    }

# Create database engine
engine = create_engine(
    database_url,
    connect_args=connect_args,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=settings.debug,
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
