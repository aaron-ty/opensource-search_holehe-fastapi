from typing import Any, Dict
from datetime import datetime, timezone
from src.core.logging import get_logger
from src.domain.models.search import EmailSearchRequest
from src.domain.models.response import (
    ModuleListResponse, SearchResponse, ResponseHeaders,
    AggregatedResponse, StandardResponse
)
from src.domain.services.email_search_service import EmailSearchService

logger = get_logger(__name__)

from src.core.config import get_settings
settings = get_settings()

class EmailController:
    """Controller for email search operations."""
    
    def __init__(self):
        self.service = EmailSearchService()
        self.service_name = f"{settings.APP_NAME} - sfera.email"
    
    async def search(
        self,
        request: EmailSearchRequest,
        only_found: bool = False
    ) -> SearchResponse:
        """
        Perform email search with Sfera-compliant response.
        """
        logger.info(f"Email search request: {request.payload}")

        # Get aggregated result from service
        aggregated_result = await self.service.search(request, only_found)
        
        # Convert to Sfera format
        return self._convert_to_sfera_format(aggregated_result, request.payload)
    
    def get_active_modules(self) -> ModuleListResponse:
        """Get list of active email modules in Sfera format."""
        modules = self.service.get_active_modules()
        logger.debug(f"Active email modules: {len(modules)}")
       
        return ModuleListResponse(
            headers=ResponseHeaders(sender=self.service_name),
            body={
                "modules": modules,
                "count": len(modules),
                "type": "email"
            },
            extra={
                "timestamp":  datetime.now(timezone.utc).replace(microsecond=0).isoformat()}
        )
    
    def get_all_modules(self) -> ModuleListResponse:
        """Get list of all email modules in Sfera format."""
        modules = self.service.get_all_modules()
        logger.debug(f"All email modules: {len(modules)}")
        return ModuleListResponse(
            headers=ResponseHeaders(sender=self.service_name),
            body={
                "modules": modules,
                "count": len(modules),
                "type": "email"
            },
            extra={
                "timestamp":  datetime.now(timezone.utc).replace(microsecond=0).isoformat()            }
        )
    
    async def search_as_standard_response(
        self,
        email: str,
        modules: list[str]
    ) -> list[StandardResponse]:
        """
        Perform email search and return in standard response format.
        Used by orchestrator.
        """
        request = EmailSearchRequest(payload=email, modules=modules)
        aggregated_result = await self.service.search(request, only_found=False)

        responses = []
        for module_name, module_result in aggregated_result.results.items():
            # Convert module result to Sfera format
            responses.append(StandardResponse(
                headers=ResponseHeaders(sender=f"{self.service_name}.{module_name}"),
                body={
                    "query": email,
                    "module": module_name,
                    "status": module_result.status,
                    "code": module_result.code,
                    "message": module_result.message,
                    "found": len(module_result.records) > 0 and module_result.code == 200,
                    "records": [record.dict() for record in module_result.records]
                },
                extra={
                    "timestamp": module_result.timestamp,
                    "data_type": "email",
                    "module_name": module_name
                }
            ))
        
        return responses
    
    def _convert_to_sfera_format(
        self, 
        aggregated_result: AggregatedResponse,
        query: str
    ) -> SearchResponse:
        """Convert aggregated result to Sfera-compliant format."""
        # Build results in Sfera format
        results = {}
        
        for module_name, module_result in aggregated_result.results.items():
            results[module_name] = {
                "status": module_result.status,
                "code": module_result.code,
                "message": module_result.message,
                "records": [record.dict() for record in module_result.records],
                "timestamp": module_result.timestamp
            }
        
        return SearchResponse(
            headers=ResponseHeaders(sender=self.service_name),
            body={
                "query": query,
                "total_modules": aggregated_result.total_modules,
                "successful": aggregated_result.successful,
                "failed": aggregated_result.failed,
                "results": results
            },
            extra={
                "timestamp": aggregated_result.timestamp,
                "data_type": "email",
                "query_type": "email_search"
            }
        )
    
    async def search_legacy_format(
        self,
        request: EmailSearchRequest,
        only_found: bool = False
    ) -> Dict[str, Any]:
        """
        Perform email search and return in legacy response format.
        """
        from src.domain.services.legacy_response_service import LegacyResponseService

        # Get modern response
        modern_response = await self.search(request, only_found)

        # Convert to legacy format for backward compatibility
        legacy_service = LegacyResponseService()
        return legacy_service.convert_to_legacy_format(modern_response)