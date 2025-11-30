# Docker One-Click Deployment Guide

This guide will help you quickly deploy the SVV-LoginPage application (including frontend and backend) using Docker.

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+

Check your installation:
```bash
docker --version
docker-compose --version
```

## Quick Start

### 1. Clone or Navigate to Project Directory

```bash
cd SVV-LoginPage
```

### 2. Configure Environment Variables (Optional)

Create a `.env` file to customize your configuration:

```bash
cp .env.example .env
```

Edit the `.env` file:

```env
# Database password (recommended to change)
DB_PASSWORD=your_secure_password_here

# JWT secret key (recommended to regenerate)
# Generate new key: openssl rand -hex 32
SECRET_KEY=your_secret_key_here

# JWT Configuration
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application ports
APP_PORT=8000
DB_PORT=5432

# Debug mode (set to False in production)
DEBUG=False
```

### 3. Start Application with One Command

```bash
docker-compose up -d
```

This command will:
- Automatically build the application image
- Start PostgreSQL database
- Start application service (including frontend and backend)
- Automatically initialize the database

### 4. Verify Deployment

Check service status:
```bash
docker-compose ps
```

View logs:
```bash
docker-compose logs -f app
```

Check health status:
```bash
curl http://localhost:8000/health
```

### 5. Access the Application

- **Frontend Page**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Common Commands

### Stop Services

```bash
docker-compose stop
```

### Start Stopped Services

```bash
docker-compose start
```

### Restart Services

```bash
docker-compose restart
```

### Stop and Remove Containers

```bash
docker-compose down
```

### Stop and Remove All Data (including database)

```bash
docker-compose down -v
```

### Rebuild Images

```bash
docker-compose build --no-cache
docker-compose up -d
```

### View Logs

```bash
# View all service logs
docker-compose logs -f

# View application logs only
docker-compose logs -f app

# View database logs only
docker-compose logs -f postgres
```

### Access Containers

```bash
# Access application container
docker-compose exec app bash

# Access database container
docker-compose exec postgres psql -U svv_user -d svv_auth
```

## Production Deployment Recommendations

### 1. Security Configuration

In production environments, make sure to modify the following configurations:

```env
# Use strong passwords
DB_PASSWORD=<strong-random-password>

# Generate new JWT secret key
SECRET_KEY=<run: openssl rand -hex 32>

# Disable debug mode
DEBUG=False
```

### 2. Use HTTPS

It's recommended to add an Nginx reverse proxy with SSL certificates:

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3. Database Backups

Regularly backup your database:

```bash
# Backup database
docker-compose exec postgres pg_dump -U svv_user svv_auth > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore database
docker-compose exec -T postgres psql -U svv_user svv_auth < backup_20231120_120000.sql
```

### 4. Resource Limits

Modify `docker-compose.yml` to add resource limits:

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 1G
        reservations:
          cpus: '1'
          memory: 512M
```

### 5. Log Management

Configure log rotation:

```yaml
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## Architecture Overview

### Multi-Stage Build

The Dockerfile uses a multi-stage build strategy:

1. **Stage 1 (frontend-builder)**: Build React frontend using Node.js
2. **Stage 2 (final)**: Set up Python backend and copy frontend build files

This approach:
- Reduces final image size
- Separates build and runtime environments
- Improves build efficiency

### Service Components

- **postgres**: PostgreSQL 15 database
- **app**: FastAPI application (including static frontend files)

### Networking

All services run in an isolated Docker network `svv-network` for security.

### Data Persistence

Database data is stored in the Docker volume `postgres_data`, ensuring data persists even if containers are deleted.

## Troubleshooting

### Application Won't Start

1. Check logs:
```bash
docker-compose logs app
```

2. Verify database connection:
```bash
docker-compose exec app python -c "from backend.database import engine; print(engine.url)"
```

### Database Connection Failed

1. Confirm database is running:
```bash
docker-compose ps postgres
```

2. Test database connection:
```bash
docker-compose exec postgres pg_isready -U svv_user
```

### Port Conflicts

If ports 8000 or 5432 are already in use, modify the `.env` file:

```env
APP_PORT=8080
DB_PORT=5433
```

Then restart:
```bash
docker-compose down
docker-compose up -d
```

### Clean Up and Start Fresh

```bash
# Stop all services
docker-compose down -v

# Remove images
docker-compose down --rmi all

# Rebuild and start
docker-compose up -d --build
```

## Performance Optimization

### 1. Use BuildKit

Enable Docker BuildKit to speed up builds:

```bash
DOCKER_BUILDKIT=1 docker-compose build
```

### 2. Cache Optimization

The Dockerfile is optimized for layer caching by copying dependency files first, then source code.

### 3. Production Optimizations

- Use Gunicorn or Uvicorn workers
- Enable Nginx static file caching
- Configure PostgreSQL connection pooling

## Updating the Application

```bash
# 1. Pull latest code
git pull

# 2. Rebuild images
docker-compose build

# 3. Restart services (zero downtime)
docker-compose up -d
```

## Monitoring

### Health Checks

Both application and database have configured health checks:

```bash
# Check health status
docker-compose ps

# Manual test
curl http://localhost:8000/health
```

### Resource Usage

```bash
# View container resource usage
docker stats
```

## Support

For issues, please refer to:
- [Main Documentation](README.md)
- [Quick Start Guide](QUICKSTART.md)
- [Simple Frontend Guide](SIMPLE_FRONTEND_GUIDE.md)

---

**Version**: 1.0.0
**Last Updated**: November 2024
