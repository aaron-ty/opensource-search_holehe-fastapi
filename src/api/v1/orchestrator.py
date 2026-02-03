from fastapi import APIRouter
from src.controllers.orchestrator_controller import OrchestratorController
from src.domain.models.orchestrator import (
    OrchestratorRequest, 
    OrchestratorResponse,
    DirectSearchRequest
)
from src.core.logging import get_logger

logger = get_logger(__name__)
from src.core.config import get_settings
settings = get_settings()
router = APIRouter(prefix=f"{settings.API_V1_PREFIX}/orchestrator", tags=["orchestrator"])

orchestrator_controller = OrchestratorController()


@router.post("/search", response_model=OrchestratorResponse)
async def orchestrator_search(request: OrchestratorRequest):
    """
    Main orchestrator endpoint that uses validator service.
    Returns Sfera-compliant response.
    """
    return await orchestrator_controller.process_with_validator(request)


@router.post("/search-direct", response_model=OrchestratorResponse)
async def orchestrator_search_direct(request: DirectSearchRequest):
    """
    Direct search endpoint that bypasses validator service.
    Returns Sfera-compliant response.
    """
    return await orchestrator_controller.process_direct(request)
