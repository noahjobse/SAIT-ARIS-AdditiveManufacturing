import contextlib
import logging
from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import thread_pool
from app.routers import kinematics, obstacles, parse, printing, robots, simulate, upload
from app.thread_pool import MAX_WORKERS

logger = logging.getLogger(__name__)


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages app startup and shutdown.
    - Startup: Initialize thread pool executor
    - Shutdown: Clean shutdown of executor
    """
    # Startup
    thread_pool.executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
    logger.info(f"Thread pool initialized with max_workers={MAX_WORKERS}")

    yield

    # Shutdown
    if thread_pool.executor:
        thread_pool.executor.shutdown(wait=True)
        logger.info("Thread pool shut down successfully")


app = FastAPI(
    title="ABB Robot Simulation Backend",
    description="FastAPI + PyBullet backend for ABB robot simulation",
    version="0.1.0",
    lifespan=lifespan
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router)
app.include_router(robots.router)
app.include_router(kinematics.router)
app.include_router(parse.router)
app.include_router(simulate.router)
app.include_router(obstacles.router)
app.include_router(printing.router)

@app.get("/")
async def root():
    return {
        "message": "ABB Robot Simulation Backend",
        "version": "0.1.0",
        "status": "running"
    }

@app.get("/api/health")
async def health():
    """Health check endpoint"""
    from datetime import datetime
    return {
        "status": "healthy",
        "version": "0.1.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/robots")
async def list_robots():
    """List all available robot models"""
    return [
        {
            "id": "irb4600",
            "name": "IRB 4600-60/2.05",
            "manufacturer": "ABB",
            "dof": 6,
            "payload_kg": 60,
            "reach_mm": 2050,
            "model_url": "/api/robots/irb4600/model"
        },
        {
            "id": "irb2600",
            "name": "IRB 2600-12/1.65",
            "manufacturer": "ABB",
            "dof": 6,
            "payload_kg": 12,
            "reach_mm": 1650,
            "model_url": "/api/robots/irb2600/model"
        },
        {
            "id": "irb6700",
            "name": "IRB 6700-145/3.2",
            "manufacturer": "ABB",
            "dof": 6,
            "payload_kg": 145,
            "reach_mm": 3200,
            "model_url": "/api/robots/irb6700/model"
        }
    ]
