import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db, Base
from app.models.todo import Todo
from app.models.preferences import GlobalPreferences

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture
def setup_database():
    """Create test database tables"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_todo_data():
    """Sample todo data for tests"""
    return {
        "text": "Complete the Death Star plans",
        "priority": "high"
    }


@pytest.fixture
def create_sample_todos(setup_database):
    """Create sample todos in the database"""
    db = TestingSessionLocal()
    todos = [
        Todo(text="Find rebel base", priority="high", completed=False),
        Todo(text="Train Stormtroopers", priority="medium", completed=True),
        Todo(text="Build new starship", priority="low", completed=False)
    ]
    for todo in todos:
        db.add(todo)
    db.commit()
    
    # Get the created todos with their IDs
    created_todos = db.query(Todo).all()
    db.close()
    return created_todos