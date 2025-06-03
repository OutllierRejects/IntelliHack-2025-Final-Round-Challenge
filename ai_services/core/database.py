# core/database.py
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from core.config import DATABASE_URL, DATABASE_ECHO
import logging

logger = logging.getLogger(__name__)

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=DATABASE_ECHO,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base
Base = declarative_base()

# Metadata for migrations
metadata = MetaData()


def get_db() -> Session:
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


@contextmanager
def get_db_session():
    """Context manager for database sessions"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Database session error: {e}")
        raise
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    try:
        # Import all models to register them with Base
        from models import user, request, task, resource, incident

        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


# Optional: Supabase client for those who want to use it
try:
    from supabase import create_client, Client
    from core.config import SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY

    if SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    else:
        supabase = None
except ImportError:
    supabase = None
