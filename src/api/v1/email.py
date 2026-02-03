from fastapi import APIRouter, Query
from src.controllers.email_controller import EmailController
from src.domain.models.search import EmailSearchRequest
from src.domain.models.response import SearchResponse, ModuleListResponse

from src.core.logging import get_logger

logger = get_logger(__name__)

from src.core.config import get_settings
settings = get_settings()
router = APIRouter(prefix=f"{settings.API_V1_PREFIX}/email", tags=["email"])

email_controller = EmailController()


@router.get("/modules/active", response_model=ModuleListResponse)
async def get_active_email_modules():
    """Get list of active email modules in Sfera format."""
    return email_controller.get_active_modules()


@router.get("/modules/all", response_model=ModuleListResponse)
async def get_all_email_modules():
    """Get list of all email modules in Sfera format."""
    return email_controller.get_all_modules()


@router.post("/search", response_model=SearchResponse)
async def search_email(
    request: EmailSearchRequest,
    only_found: bool = Query(False, description="Return only modules with found data")
):
    """
    Search for email across multiple modules in Sfera format.
    """
    return await email_controller.search(request, only_found)


"""@router.post("/search-legacy")
async def search_email_legacy(
    request: EmailSearchRequest,
    only_found: bool = Query(False, description="Return only modules with found data")
):
    
    #Search for email across multiple modules (legacy compatible).
   
    return await email_controller.search_legacy_format(request, only_found)"""