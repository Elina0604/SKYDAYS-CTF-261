from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from .config import settings
from .database import engine, Base, SessionLocal
from .routers import todos, preferences
from .models.todo import Todo
from .models.flag import Flag
from .models.preferences import GlobalPreferences
from .utils.exceptions import (
    validation_exception_handler,
    http_exception_handler, 
    sqlalchemy_exception_handler,
    general_exception_handler
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize database with CTF flag and sample data
def init_database():
    """Initialize database with CTF challenge data"""
    db = SessionLocal()
    try:
        # Check if flag already exists
        existing_flag = db.query(Flag).first()
        if not existing_flag:
            # Insert the CTF flag
            flag = Flag(
                flag_value="SKYDAYS{SKYORDER_66_HAD_TO_EXECUTED}",
                description="Execute Order 66 - The hidden Imperial intelligence"
            )
            db.add(flag)
            
            # Add some sample todos to make the challenge more realistic
            sample_todos = [
                Todo(text="Prepare the Death Star plans", priority="high", completed=False),
                Todo(text="Train new Stormtroopers", priority="medium", completed=True),
                Todo(text="Schedule meeting with Emperor", priority="high", completed=False),
                Todo(text="Review rebel intelligence reports", priority="low", completed=False),
                Todo(text="Inspect Imperial fleet", priority="medium", completed=True),
            ]
            
            for todo in sample_todos:
                db.add(todo)
            
            db.commit()
            print("🏴 CTF Challenge initialized! Flag planted in the Empire's database...")
        else:
            print("🏴 CTF Challenge already initialized")
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

# Initialize the database
init_database()

# Create FastAPI app
app = FastAPI(
    title="🏴 Order 66: Execute the Query - CTF Challenge",
    description="The Galactic Empire's task management system. Intelligence suggests that critical information is hidden within their database...",
    version="1.0.0-CTF",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include routers
app.include_router(todos.router, prefix="/api", tags=["todos"])
app.include_router(preferences.router, prefix="/api", tags=["preferences"])


@app.get("/")
async def root():
    return {
        "message": "🏴 Welcome to the Empire's Task Management System", 
        "mission": "Intelligence suggests critical information is hidden in the database...",
        "hint": "The sorting functionality seems particularly interesting...",
        "docs": "/docs",
        "target": "Extract the hidden Imperial intelligence",
        "flag_format": "SKYDAYS{...}"
    }


@app.get("/api/health")
async def health():
    return {"status": "operational", "message": "The Empire's systems are fully operational"}


@app.get("/api/info")
async def info():
    return {
        "challenge": "🏴 Order 66: Execute the Query",
        "version": "1.0.0-CTF",
        "description": "The Galactic Empire's task management system",
        "mission": "Extract hidden Imperial intelligence from the database",
        "endpoints": {
            "docs": "/docs",
            "health": "/api/health", 
            "todos": "/api/todos - Try different sort parameters!",
            "preferences": "/api/preferences"
        },
        "hint": "The Force suggests examining the sorting functionality... May contain sensitive Imperial data."
    }