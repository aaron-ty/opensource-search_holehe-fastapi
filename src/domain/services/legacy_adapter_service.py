from typing import List, Any
from src.core.logging import get_logger
from src.domain.models.response import DataRecord
from src.core.constants import ResultCode

logger = get_logger(__name__)

class LegacyAdapterService:
    """
    Faithfully replicates the legacy DefaultHoleheAdapter logic
    Preserves 100% of original business logic
    """
    
    @staticmethod
    def cast_holehe_to_isphere(output: List[dict]) -> List[DataRecord]:
        """
        Exact replica of legacy DefaultHoleheAdapter.cast_holehe_to_isphere
        """
        response = output[0] if output else None

        if not response:
            return []

        # Handle rate limiting (legacy logic)
        if response.get("rateLimit"):
            from src.domain.exceptions import RateLimitException
            raise RateLimitException("Ошибка внутри использования модуля")

        # Handle no data found (legacy logic)
        if not response.get("exists"):
            from src.domain.exceptions import NoDataFoundException
            raise NoDataFoundException()

        # Legacy output structure
        output_data = {
            "result": "Найден",
            "result_code": "FOUND",
        }

        # Legacy field mappings
        if response.get("phoneNumber"):
            output_data["phone_number"] = response["phoneNumber"]

        if response.get("emailrecovery"):
            output_data["email_recovery"] = response["emailrecovery"]

        if response.get("others"):
            output_data.update(response.get("others"))

        return [DataRecord(**output_data)]
    
    @staticmethod
    def cast_ignorant_to_isphere(output: List[dict]) -> List[DataRecord]:
        """
        Adapt ignorant module output using legacy patterns
        """
        if not output:
            return []
            
        response = output[0] if output else {}
        
        # Handle rate limiting
        if response.get("rateLimit"):
            from src.domain.exceptions import RateLimitException
            raise RateLimitException("Rate limit exceeded in module")
        
        # Handle no data
        if not response.get("exists", False):
            from src.domain.exceptions import NoDataFoundException
            raise NoDataFoundException()
        
        # Build legacy-compatible output
        output_data = {
            "result": "Найден",
            "result_code": "FOUND",
        }
        
        # Map ignorant-specific fields
        if response.get("phone"):
            output_data["phone_number"] = response["phone"]
            
        if response.get("email"):
            output_data["email_recovery"] = response["email"]
            
        return [DataRecord(**output_data)]