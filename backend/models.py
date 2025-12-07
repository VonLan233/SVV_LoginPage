"""
SVV-LoginPage Database Models
SQLAlchemy ORM models for user authentication
"""

from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from backend.database import Base


class User(Base):
    """User model for authentication

    Attributes:
        id: Primary key
        username: Unique username for login (max 100 chars)
        email: Unique email address (max 255 chars)
        hashed_password: Bcrypt hashed password
        is_active: Whether the user account is active
        is_superuser: Whether the user has superuser privileges
        created_at: Timestamp of account creation
        updated_at: Timestamp of last update
        token_version: Incremented on password change to invalidate existing tokens
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    token_version = Column(Integer, default=0, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"
