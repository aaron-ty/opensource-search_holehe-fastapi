from typing import List
from src.core.logging import get_logger
from src.domain.models.response import DataRecord
from src.domain.services.legacy_adapter_service import LegacyAdapterService
from src.domain.exceptions import NoDataFoundException, RateLimitException

logger = get_logger(__name__)

class ModuleAdapterService:
    """Enhanced adapter service using legacy business logic."""
    
    def __init__(self):
        self.legacy_adapter = LegacyAdapterService()
    
    def adapt_holehe_result(self, output: List[dict]) -> List[DataRecord]:
        """
        Adapt holehe module output using legacy business logic.
        """
        try:
            return self.legacy_adapter.cast_holehe_to_isphere(output)
        except RateLimitException as e:
            logger.warning(f"Rate limited in module: {str(e)}")
            raise
        except NoDataFoundException as e:
            logger.info(f"No data found in module")
            raise
        except Exception as e:
            logger.error(f"Adapter error: {str(e)}")
            raise
    
    def adapt_ignorant_result(self, output: List[dict]) -> List[DataRecord]:
        """
        Adapt ignorant module output using legacy patterns.
        """
        try:
            return self.legacy_adapter.cast_ignorant_to_isphere(output)
        except RateLimitException as e:
            logger.warning(f"Rate limited in module: {str(e)}")
            raise
        except NoDataFoundException as e:
            logger.info(f"No data found in module")
            raise
        except Exception as e:
            logger.error(f"Adapter error: {str(e)}")
            raise