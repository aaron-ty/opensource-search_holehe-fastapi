from fastapi import APIRouter, Query
from src.controllers.phone_controller import PhoneController
from src.domain.models.search import PhoneSearchRequest
from src.domain.models.response import SearchResponse, ModuleListResponse

from src.core.logging import get_logger

logger = get_logger(__name__)
from src.core.config import get_settings
settings = get_settings()
router = APIRouter(prefix=f"{settings.API_V1_PREFIX}/phone", tags=["phone"])

phone_controller = PhoneController()


@router.get("/modules/active", response_model=ModuleListResponse)
async def get_active_phone_modules():
    """Get list of active phone modules."""
    return phone_controller.get_active_modules()


@router.get("/modules/all", response_model=ModuleListResponse)
async def get_all_phone_modules():
    """Get list of all phone modules."""
    return phone_controller.get_all_modules()


@router.post("/search", response_model=SearchResponse)
async def search_phone(
    request: PhoneSearchRequest,
    only_found: bool = Query(False, description="Return only modules with found data")
):
    """
    Search for phone number across multiple modules.
    
    - **payload**: Phone number to search
    - **modules**: List of module names or ["*"] for all active modules
    - **timeout**: Optional timeout in seconds
    - **only_found**: If true, only return results where data was found
    """
    return await phone_controller.search(request, only_found)

"""
@router.post("/search-legacy")  # FIXED: Changed from duplicate "/search"
async def search_phone_legacy(
    request: PhoneSearchRequest,
    only_found: bool = Query(False, description="Return only modules with found data")
):
    
    #Search for phone number across multiple modules (legacy compatible).
    
    #- **payload**: Phone number to search
    #- **modules**: List of module names or ["*"] for all active modules
    #- **timeout**: Optional timeout in seconds
    #- **only_found**: If true, only return results where data was found
    
    return await phone_controller.search_legacy_format(request, only_found)"""