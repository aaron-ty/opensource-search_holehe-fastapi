from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from src.domain.models.response import StandardResponse, ResponseHeaders
from src.domain.exceptions import DomainException
from src.core.logging import get_logger
import traceback
from datetime import datetime, timezone
from src.core.config import get_settings
settings = get_settings()


logger = get_logger(__name__)


async def sfera_validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors in Sfera format."""
    logger.warning(f"Validation error: {exc.errors()}")
    
    error_response = StandardResponse(
        headers=ResponseHeaders(sender=f"{settings.APP_NAME} - sfera.core"),
        body={
            "error": "Invalid request data",
            "details": exc.errors(),
            "status": "error"
        },
        extra={
            "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "path": str(request.url)
        }
    )
    
    return JSONResponse(
        status_code=400,
        content=error_response.dict()
    )


async def sfera_domain_exception_handler(request: Request, exc: DomainException):
    """Handle domain exceptions in Sfera format."""
    logger.warning(f"Domain exception: {exc.message}")
    
    error_response = StandardResponse(
        headers=ResponseHeaders(sender=f"{settings.APP_NAME} - sfera.core"),
        body={
            "error": exc.message,
            "status": "error"
        },
        extra={
            "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "path": str(request.url)
        }
    )
    
    return JSONResponse(
        status_code=exc.code,
        content=error_response.dict()
    )


async def sfera_general_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions in Sfera format."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    # Don't expose internal details in production
    message = str(exc)  # You might want to genericize this in production
    
    error_response = StandardResponse(
        headers=ResponseHeaders(sender=f"{settings.APP_NAME} - sfera.core"),
        body={
            "error": message,
            "status": "error"
        },
        extra={
            "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "path": str(request.url)
        }
    )
    
    return JSONResponse(
        status_code=500,
        content=error_response.dict()
    )


async def legacy_exception_handler(request: Request, exc: Exception):
    """Legacy exception handler for backward compatibility."""
    from src.domain.services.legacy_response_service import LegacyResponseService
    
    legacy_service = LegacyResponseService()
    
    # Determine appropriate status code
    if hasattr(exc, 'code'):
        status_code = exc.code
    else:
        status_code = 500
    
    error_response = legacy_service.create_legacy_error_response(
        error_message=str(exc),
        code=status_code
    )
    
    return JSONResponse(
        status_code=status_code,
        content=error_response
    )