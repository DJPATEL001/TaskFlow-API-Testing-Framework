from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base, SessionLocal
from app.models.user import User
from app.seed import seed_database
from app.routers import (
    auth_router,
    projects_router,
    tasks_router,
    users_router,
    dashboard_router,
)

app = FastAPI(
    title="TaskFlow API",
    description="A professional REST API for task and project management, built with FastAPI, SQLAlchemy, and SQLite/MySQL compatibility.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for local testing and frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(tasks_router)
app.include_router(users_router)
app.include_router(dashboard_router)


@app.on_event("startup")
def startup_event():
    """Ensure database tables exist and seed default data if database is empty."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        user_count = db.query(User).count()
        if user_count == 0:
            print("Database is empty. Running seed_database()...")
            seed_database()
    finally:
        db.close()


@app.get("/", tags=["Health Check"])
def root():
    return {
        "message": "Welcome to TaskFlow REST API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }
