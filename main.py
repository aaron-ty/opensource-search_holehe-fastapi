from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.core.config import get_settings
from src.core.logging import setup_logging, get_logger
from src.core.constants import ResponseStatus, HTTP_STATUS_BAD_REQUEST, HTTP_STATUS_INTERNAL_ERROR
from src.core.exception_handlers import (
    sfera_validation_exception_handler,
    sfera_domain_exception_handler, 
    sfera_general_exception_handler
)
from src.api.v1.email import router as router_email
from src.api.v1.phone import router as router_phone
from src.api.v1.orchestrator import router as router_orchestrator
from src.domain.exceptions import DomainException
from src.domain.models.response import HealthResponse, ResponseHeaders

# Setup logging
setup_logging()
logger = get_logger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Mode: {settings.MODE}")
    logger.info(f"Debug: {settings.DEBUG}")
    
    yield
    
    # Shutdown
    logger.info(f"Shutting down {settings.APP_NAME}")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="OSINT service for email and phone number searches",
    lifespan=lifespan,
    debug=settings.DEBUG
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers for modern endpoints
app.add_exception_handler(RequestValidationError, sfera_validation_exception_handler)
app.add_exception_handler(DomainException, sfera_domain_exception_handler)
app.add_exception_handler(Exception, sfera_general_exception_handler)

# Include routers
app.include_router(router_email)
app.include_router(router_phone)
app.include_router(router_orchestrator)

logger.info("Sfera OSINT Service started successfully")


@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint."""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs" : "/docs",
        "status": "running"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint in Sfera format."""
    settings = get_settings()
    return HealthResponse(
        headers=ResponseHeaders(sender=f"{settings.APP_NAME} - sfera.core"),
        body={
            "status": "ok",
            "version": settings.APP_VERSION,
            "service": settings.APP_NAME
        },
        extra={
            "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "mode": settings.MODE
        }
    )


@app.get("/status", response_model=HealthResponse)
async def status_check():
    """Status check endpoint in Sfera format."""
    settings = get_settings()
    return HealthResponse(
        headers=ResponseHeaders(sender=f"{settings.APP_NAME} - sfera.core"),
        body={
            "status": "ok", 
            "version": settings.APP_VERSION,
            "service": settings.APP_NAME
        },
        extra={
            "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "mode": settings.MODE
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        workers=settings.WORKERS,
        reload=settings.DEBUG,
        log_level="info"
    )