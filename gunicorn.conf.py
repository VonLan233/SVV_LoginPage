# Gunicorn configuration for multi-core parallel processing
import multiprocessing
import os

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"

# Worker processes
# Recommended formula: 2 * CPU cores + 1
# Can be overridden with GUNICORN_WORKERS env var
_workers_env = os.environ.get("GUNICORN_WORKERS", "")
workers = int(_workers_env) if _workers_env else multiprocessing.cpu_count() * 2 + 1

# Use uvicorn workers for async support
worker_class = "uvicorn.workers.UvicornWorker"

# Worker timeout (seconds)
timeout = 120

# Keep-alive connections
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = os.environ.get("LOG_LEVEL", "info")

# Process naming
proc_name = "svv-loginpage"

# Preload app for memory efficiency (shared memory between workers)
preload_app = True

# Graceful restart timeout
graceful_timeout = 30

# Max requests per worker before restart (prevents memory leaks)
max_requests = 1000
max_requests_jitter = 50
