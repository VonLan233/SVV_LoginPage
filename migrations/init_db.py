"""
SVV-LoginPage Database Initialization Script

Creates the users table and optionally creates an admin user.

Usage:
    python init_db.py                    # Just create tables
    python init_db.py --create-admin     # Create tables and admin user
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import backend module
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.database import engine, Base, SessionLocal
from backend.models import User
from backend.auth import get_password_hash


def init_database():
    """Initialize database by creating all tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully!")


def create_admin_user(username="admin", email="admin@example.com", password="admin123"):
    """Create an admin user"""
    db = SessionLocal()
    try:
        # Check if admin user already exists
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            print(f"✓ Admin user '{username}' already exists")
            return

        # Create admin user
        admin_user = User(
            username=username,
            email=email,
            hashed_password=get_password_hash(password),
            is_active=True,
            is_superuser=True
        )
        db.add(admin_user)
        db.commit()
        print(f"✓ Admin user created:")
        print(f"  Username: {username}")
        print(f"  Email: {email}")
        print(f"  Password: {password}")
        print(f"  IMPORTANT: Change this password after first login!")
    except Exception as e:
        db.rollback()
        print(f"✗ Error creating admin user: {e}")
    finally:
        db.close()


def main():
    """Main entry point"""
    print("\n=== SVV-LoginPage Database Initialization ===\n")

    # Initialize database
    init_database()

    # Check if --create-admin flag is provided
    if "--create-admin" in sys.argv:
        print("\nCreating admin user...")
        create_admin_user()
    else:
        print("\nSkipping admin user creation.")
        print("Run with --create-admin to create default admin user")

    print("\n=== Initialization Complete ===\n")


if __name__ == "__main__":
    main()
