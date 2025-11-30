"""
SVV-LoginPage Database Connection
SQLAlchemy database engine and session management
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from backend.config import settings

# Create database engine
# Handle SQLite vs PostgreSQL differences
if settings.database_url.startswith("sqlite"):
    # SQLite configuration
    engine = create_engine(
        settings.database_url,
        echo=settings.debug,
        connect_args={"check_same_thread": False}
    )
else:
    # PostgreSQL configuration
    engine = create_engine(
        settings.database_url,
        echo=settings.debug,
        pool_pre_ping=True,
        pool_recycle=300
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for declarative models
Base = declarative_base()


def get_db():
    """Dependency function to get database session

    Usage in FastAPI endpoints:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()

    Yields:
        SQLAlchemy Session object

    Ensures:
        Database session is properly closed after request
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables

    Creates all tables defined in models.py.
    Should be called once during application startup.

    Example:
        from backend.database import init_db
        init_db()
    """
    # Import models to ensure they are registered with Base
    from backend.models import User

    # Create all tables
    Base.metadata.create_all(bind=engine)
