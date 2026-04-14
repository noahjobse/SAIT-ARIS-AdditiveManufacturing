"""
Production Gunicorn configuration for ArmStudio backend.

Usage:
    gunicorn app.main:app -c gunicorn.conf.py

Gunicorn manages multiple uvicorn worker processes.
Each worker runs an asyncio event loop with its own PyBullet physics client.
PYBULLET_THREADS controls the thread pool within each worker.
"""
import os

# Worker class: uvicorn's ASGI worker (wraps uvicorn in a gunicorn worker)
worker_class = "uvicorn.workers.UvicornWorker"

# Number of worker processes. Defaults to 2.
# Each worker gets its own PyBullet physics client.
# NOTE: PyBullet is not thread-safe across processes, but each process is isolated.
workers = int(os.environ.get("WEB_WORKERS", "2"))

# Threads per worker process (for non-async blocking calls)
threads = 1  # uvicorn handles concurrency via asyncio, not threads

# Bind address
bind = os.environ.get("GUNICORN_BIND", "0.0.0.0:8000")

# Timeout in seconds — IK/trajectory generation can take up to 30s
timeout = int(os.environ.get("GUNICORN_TIMEOUT", "60"))

# Keep-alive connections
keepalive = 5

# Graceful shutdown timeout
graceful_timeout = 30

# Logging
loglevel = os.environ.get("LOG_LEVEL", "info")
accesslog = "-"  # stdout
errorlog = "-"   # stderr
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s %(D)sμs'
