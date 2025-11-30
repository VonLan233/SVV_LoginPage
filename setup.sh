#!/bin/bash

echo "============================================"
echo "SVV-LoginPage Local Setup Script"
echo "============================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo "Checking prerequisites..."

command -v python3 >/dev/null 2>&1 || { echo -e "${RED}Error: Python 3 is not installed${NC}"; exit 1; }
command -v node >/dev/null 2>&1 || { echo -e "${RED}Error: Node.js is not installed${NC}"; exit 1; }
command -v psql >/dev/null 2>&1 || { echo -e "${RED}Error: PostgreSQL is not installed${NC}"; exit 1; }

echo -e "${GREEN}✓ All prerequisites found${NC}"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}Warning: .env file not found${NC}"
    echo "Copying .env.example to .env..."
    cp .env.example .env
    echo -e "${YELLOW}Please edit .env file with your database credentials before continuing${NC}"
    echo "Press Enter to continue after editing .env, or Ctrl+C to exit..."
    read
fi

# Load environment variables
source .env

# Setup PostgreSQL database
echo "Setting up PostgreSQL database..."
echo "Please enter your PostgreSQL admin password when prompted:"

psql -U postgres -c "CREATE DATABASE svv_auth;" 2>/dev/null || echo "Database may already exist, continuing..."
psql -U postgres -c "CREATE USER svv_user WITH PASSWORD 'svv_password_change_me';" 2>/dev/null || echo "User may already exist, continuing..."
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE svv_auth TO svv_user;" 2>/dev/null

echo -e "${GREEN}✓ Database setup complete${NC}"
echo ""

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r backend/requirements.txt
echo -e "${GREEN}✓ Python dependencies installed${NC}"
echo ""

# Initialize database
echo "Initializing database tables..."
python -c "from backend.database import init_db; init_db()"
echo -e "${GREEN}✓ Database initialized${NC}"
echo ""

# Install and build frontend
echo "Installing frontend dependencies..."
cd frontend-example
npm install
echo -e "${GREEN}✓ Frontend dependencies installed${NC}"
echo ""

echo "Building frontend..."
npm run build
echo -e "${GREEN}✓ Frontend built${NC}"
cd ..
echo ""

echo "============================================"
echo -e "${GREEN}Setup Complete!${NC}"
echo "============================================"
echo ""
echo "To start the application, run:"
echo "  ./start.sh"
echo ""
echo "Or manually run:"
echo "  python example_app.py"
echo ""
