from sqlalchemy.orm import Session
from ..database import get_db

def get_database() -> Session:
    """Dependency to get database session"""
    return next(get_db())