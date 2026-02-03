import httpx
from typing import Any, List
import re
import phonenumbers
from email_validator import validate_email, EmailNotValidError

from src.core.logging import get_logger
from src.domain.exceptions import ExternalServiceException
from src.core.constants import DataType

from src.core.config import get_settings
settings = get_settings()
logger = get_logger(__name__)

class DirectValidator:
    """
    Direct validation fallback when external validator fails.
    Implements same validation logic as legacy system.
    DIRECT CONNECTION ONLY - no external dependencies.
    """
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format directly."""
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number format directly."""
        try:
            # Clean phone number
            cleaned_phone = re.sub(r'[^\d+]', '', phone)
            if not cleaned_phone.startswith('+'):
                cleaned_phone = '+' + cleaned_phone
                
            parsed = phonenumbers.parse(cleaned_phone, None)
            return phonenumbers.is_valid_number(parsed)
        except:
            return False
    
    def validate(self, query: str) -> dict[str, Any]:
        """Direct validation with legacy-compatible output."""
        clean_query = query.strip()
        
        # Email detection
        if '@' in clean_query and self.validate_email(clean_query):
            return {
                "type": DataType.EMAIL,
                "clean_data": clean_query,
                "extra": {
                    "domain": clean_query.split('@')[-1],
                    "body_email": clean_query.split('@')[0]
                }
            }
        
        # Phone detection
        if self.validate_phone(clean_query):
            try:
                # Basic phone info extraction
                cleaned_phone = re.sub(r'[^\d+]', '', clean_query)
                if not cleaned_phone.startswith('+'):
                    cleaned_phone = '+' + cleaned_phone
                    
                return {
                    "type": DataType.PHONE,
                    "clean_data": cleaned_phone,
                    "extra": {
                        "country_code": "7",  # Default for legacy compatibility
                        "operator": "Unknown",
                        "correct_length": True
                    }
                }
            except:
                pass
        
        # Fallback for unknown types
        return {
            "type": DataType.UNKNOWN,
            "clean_data": clean_query,
            "extra": {}
        }

class ValidatorClient:
    """Enhanced validator with proper fallback mechanism and DIRECT bypass."""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url.rstrip("/") if base_url else None
        self.endpoint = f"{self.base_url}{settings.API_V1_PREFIX}/validate" if base_url else None
        self.direct_validator = DirectValidator()
        logger.info(f"Validator initialized: External={bool(self.base_url)}, DirectFallback=AlwaysAvailable")
    
    async def validate(self, query: str) -> dict[str, Any]:
        """
        Validate with external service fallback to DIRECT validation.
        Provides guaranteed direct connection bypass.
        """
        #   OPTION 1: Try external validator first if configured
        if self.base_url:
            try:
                result = await self._validate_external(query)
                if result and result.get("type") != DataType.UNKNOWN:
                    logger.info(f"Used external validator for: {query}")
                    return result
            except Exception as e:
                logger.warning(f"External validator failed, using DIRECT: {str(e)}")
        
        #   OPTION 2: Always available DIRECT connection bypass
        logger.info(f"Using DIRECT validation bypass for: {query}")
        return self.direct_validator.validate(query)
    
    async def validate_direct_only(self, query: str) -> dict[str, Any]:
        """
        DIRECT CONNECTION BYPASS - completely skip external validation.
        This fulfills the requirement for direct connection that bypasses validation.
        """
        logger.info(f"DIRECT BYPASS: Validating without external service: {query}")
        return self.direct_validator.validate(query)
    
    async def _validate_external(self, query: str) -> dict[str, Any]:
        """Validate using external service with DIRECT HTTP connection."""
        try:
            # Use direct HTTP connection (no proxy)
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.post(
                    self.endpoint,
                    json={"query": [query]}
                )
                response.raise_for_status()
                results = response.json()
                
                if results and len(results) > 0:
                    result = results[0]
                    body = result.get("body", {})
                    extra = result.get("extra", {})
                    
                    return {
                        "type": body.get("type", DataType.UNKNOWN),
                        "clean_data": body.get("clean_data", query),
                        "extra": extra
                    }
                
                return self.direct_validator.validate(query)
        
        except Exception as e:
            logger.error(f"Validator service error: {str(e)}")
            raise ExternalServiceException("validator", str(e))