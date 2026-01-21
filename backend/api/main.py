"""FastAPI main application."""
import logging
import os
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config import config
from api.routers import tasks, webhook
from database import close_db, init_db

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    
    Args:
        app: FastAPI application
    """
    # Startup
    logger.info("Starting FastAPI application...")
    try:
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        sys.exit(1)
    
    yield
    
    # Shutdown
    logger.info("Shutting down FastAPI application...")
    await close_db()
    logger.info("Database connections closed")


# Create FastAPI application
app = FastAPI(
    title="Task Tracker API",
    description="API for Telegram Task Tracker Bot with Web App",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.frontend_url, "*"],  # Allow frontend and wildcard for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
# Webhook only needed in production
if os.getenv("USE_WEBHOOK", "false").lower() == "true":
    app.include_router(webhook.router)
    logger.info("Webhook router enabled")
else:
    logger.info("Webhook router disabled (using polling mode)")

app.include_router(tasks.router)


@app.get("/")
async def root() -> dict:
    """
    Root endpoint.
    
    Returns:
        dict: Welcome message
    """
    return {
        "message": "Task Tracker API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check() -> dict:
    """
    Health check endpoint.
    
    Returns:
        dict: Health status
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "api.main:app",
        host=config.api_host,
        port=config.api_port,
        reload=True,
        log_level=config.log_level.lower(),
    )
