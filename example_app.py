"""
SVV-LoginPage Example Application

A minimal FastAPI application demonstrating how to use SVV-LoginPage.

Usage:
    python example_app.py

Then visit:
    - API docs: http://localhost:8000/docs
    - Register: POST http://localhost:8000/api/auth/register
    - Login: POST http://localhost:8000/api/auth/token
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend import router
from backend.database import init_db

# Create FastAPI app
app = FastAPI(
    title="SVV-LoginPage Example",
    description="Example application using SVV-LoginPage authentication module",
    version="1.0.0"
)

# Configure CORS
# Allow Cloud Run URL and local dev servers
cors_origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]
# Add Cloud Run URL if set
if os.environ.get("CLOUD_RUN_URL"):
    cors_origins.append(os.environ.get("CLOUD_RUN_URL"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication routes
app.include_router(router)

# Serve static files (frontend build)
STATIC_DIR = "static"
if os.path.exists(STATIC_DIR):
    app.mount("/assets", StaticFiles(directory=f"{STATIC_DIR}/assets"), name="assets")

    # Serve index.html for root and all non-API routes (SPA fallback)
    @app.get("/")
    async def serve_frontend():
        return FileResponse(f"{STATIC_DIR}/index.html")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Don't intercept API routes
        if full_path.startswith("api/") or full_path.startswith("docs") or full_path.startswith("health"):
            return {"error": "Not found"}

        # Check if file exists in static directory
        file_path = f"{STATIC_DIR}/{full_path}"
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)

        # Otherwise, serve index.html (SPA fallback)
        return FileResponse(f"{STATIC_DIR}/index.html")
else:
    # Fallback if static directory doesn't exist
    @app.get("/")
    async def root():
        return {
            "message": "SVV-LoginPage Example API",
            "docs": "/docs",
            "endpoints": {
                "register": "POST /api/auth/register",
                "login": "POST /api/auth/token",
                "current_user": "GET /api/auth/users/me",
                "update_user": "PUT /api/auth/users/me"
            }
        }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    print("\n" + "="*60)
    print("🚀 Starting SVV-LoginPage Example Application")
    print("="*60)
    print("\nInitializing database...")

    # Initialize database (create tables)
    try:
        init_db()
        print("✓ Database initialized successfully!")
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
        print("\nMake sure:")
        print("1. PostgreSQL is running")
        print("2. DATABASE_URL in .env is correct")
        print("3. Database exists")
        exit(1)

    print("\n" + "="*60)
    print("📚 API Documentation: http://localhost:8000/docs")
    print("❤️  Health Check: http://localhost:8000/health")
    print("="*60 + "\n")

    # Run the application
    # Cloud Run sets PORT env var
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
