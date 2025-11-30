# ==================================
# Stage 1: Build Frontend
# ==================================
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy all frontend files
COPY frontend-example/ ./

# Install dependencies (including dev deps needed for build)
RUN npm install

# Build frontend for production
RUN npm run build

# ==================================
# Stage 2: Setup Backend
# ==================================
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libffi-dev \
    python3-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY backend/requirements.txt ./backend/

# Install Python dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend source
COPY backend/ ./backend/
COPY example_app.py ./
COPY migrations/ ./migrations/

# Copy built frontend from previous stage
COPY --from=frontend-builder /app/frontend/dist ./static

# Create a startup script
RUN echo '#!/bin/bash\n\
echo "================================="\n\
echo "Starting SVV-LoginPage Application"\n\
echo "================================="\n\
echo ""\n\
echo "Waiting for database..."\n\
sleep 5\n\
echo ""\n\
echo "Initializing application..."\n\
python example_app.py\n\
' > /app/start.sh && chmod +x /app/start.sh

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Run the application
CMD ["/app/start.sh"]
