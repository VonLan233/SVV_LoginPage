#!/bin/bash

echo "============================================"
echo "Starting SVV-LoginPage Application"
echo "============================================"
echo ""

# Colors
GREEN='\033[0;32m'
NC='\033[0m'

# Check if setup was run
if [ ! -d "frontend-example/node_modules" ]; then
    echo "Error: Dependencies not installed. Please run ./setup.sh first"
    exit 1
fi

# Start the application
echo "Starting application..."
echo ""
echo -e "${GREEN}Application will be available at:${NC}"
echo "  - Frontend & API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python example_app.py
