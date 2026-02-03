from typing import Dict, Any
from src.domain.models.response import SearchResponse, ModuleResult, AggregatedResponse
from src.core.constants import ResponseStatus, HTTP_STATUS_OK, HTTP_STATUS_NO_CONTENT
from src.infrastructure.response_builders.legacy_response_builder import LegacyResponseBuilder
from src.core.logging import get_logger

logger = get_logger(__name__)


class LegacyResponseService:
    """Service for converting responses to exact legacy format."""
    
    def convert_to_legacy_format(self, modern_response: Any) -> Dict[str, Any]:
        """
        Convert modern Sfera response to legacy format.
        This handles both SearchResponse and other modern formats.
        """
        # If it's already a dict (like from legacy endpoints), return as-is
        if isinstance(modern_response, dict):
            return modern_response
        
        # If it's a SearchResponse, convert to legacy format
        if hasattr(modern_response, 'body') and hasattr(modern_response, 'headers'):
            return self._convert_search_response_to_legacy(modern_response)
        
        # Default case - return as dict if possible
        try:
            return modern_response.dict()
        except:
            return {"error": "Unable to convert response to legacy format"}
    
    def _convert_search_response_to_legacy(self, search_response: SearchResponse) -> Dict[str, Any]:
        """Convert SearchResponse to legacy format."""
        legacy_responses = {}
        
        # Extract results from the modern response body
        results = search_response.body.get("results", {})
        
        for module_name, module_data in results.items():
            # Build legacy SearchResponse using the legacy builder
            if module_data.get("status") == "error":
                legacy_response = LegacyResponseBuilder.error(
                    Exception(module_data.get("message", "Unknown error")),
                    module_data.get("code", 500)
                )
            else:
                legacy_response = LegacyResponseBuilder.ok(module_data.get("records", []))
                
                # Add additional fields that were in the legacy response
                legacy_response.update({
                    "status": module_data.get("status", "ok"),
                    "code": module_data.get("code", 200),
                    "message": module_data.get("message", "ok"),
                    "timestamp": module_data.get("timestamp")
                })
            
            legacy_responses[module_name] = legacy_response
        
        #   LEGACY BEHAVIOR: If single module, return directly
        if len(legacy_responses) == 1:
            return next(iter(legacy_responses.values()))
        
        return legacy_responses
    
    def create_legacy_error_response(self, error_message: str, code: int = 500) -> Dict[str, Any]:
        """Create error response in exact legacy format."""
        return LegacyResponseBuilder.error(Exception(error_message), code)
    
    def create_legacy_success_response(self, data: Any) -> Dict[str, Any]:
        """Create success response in exact legacy format."""
        return LegacyResponseBuilder.ok(data)