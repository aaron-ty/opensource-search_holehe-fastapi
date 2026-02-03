from datetime import datetime, timezone
from typing import Any, Dict, List
from src.domain.models.response import SearchResponse, DataRecord
from src.core.constants import ResponseStatus, ResultCode
from src.core.logging import get_logger

logger = get_logger(__name__)

class LegacyResponseBuilder:
    """
    Faithfully replicates KeyDBResponseBuilder from legacy system
    Preserves exact response formats and error handling
    """
    
    @staticmethod
    def ok(data: Any) -> Dict[str, Any]:
        """
        Replicate KeyDBResponseBuilder.ok() behavior
        """
        if isinstance(data, list) and data:
            # Handle list of records
            records = [record.dict() if hasattr(record, 'dict') else record for record in data]
        else:
            records = []
        
        return {
            "status": ResponseStatus.OK,
            "code": 200,
            "message": "ok",
            "records": records,
            "timestamp":  datetime.now(timezone.utc).replace(microsecond=0).isoformat()        }
    
    @staticmethod
    def error(e: Exception, code: int = 500) -> Dict[str, Any]:
        """
        Replicate KeyDBResponseBuilder.error() behavior
        """
        # Legacy error message extraction
        if hasattr(e, 'to_response'):
            message = e.to_response()
        else:
            message = str(e)
            
        if hasattr(e, 'code'):
            code = e.code
        
        return {
            "status": ResponseStatus.ERROR,
            "code": code,
            "message": message,
            "records": [],
            "timestamp":  datetime.now(timezone.utc).replace(microsecond=0).isoformat()        }
    
    @staticmethod
    def build_module_result(module_name: str, result: Any) -> Dict[str, Any]:
        """
        Build module-specific result in legacy format
        """
        if isinstance(result, tuple) and len(result) == 2:
            # Error case: (code, message)
            return LegacyResponseBuilder.error(Exception(result[1]), result[0])
        else:
            # Success case
            return LegacyResponseBuilder.ok(result)