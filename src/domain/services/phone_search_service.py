import asyncio
from typing import Optional
import phonenumbers

from src.core.constants import (
    ResponseStatus, MODULE_ALL, HTTP_STATUS_OK,
    HTTP_STATUS_NO_CONTENT, HTTP_STATUS_INTERNAL_ERROR
)
from src.core.logging import get_logger
from src.domain.exceptions import (
    ModuleNotFoundException, ModuleInactiveException,
    NoDataFoundException, RateLimitException, ValidationException
)
from src.domain.models.search import PhoneSearchRequest
from src.domain.models.response import ModuleResult, AggregatedResponse
from src.domain.services.module_adapter_service import ModuleAdapterService
from src.infrastructure.modules.holehe_modules import (
    get_ignorant_module, get_active_ignorant_modules, get_all_ignorant_modules
)

logger = get_logger(__name__)


class PhoneSearchService:
    """Service for performing phone searches across modules."""
    
    def __init__(self):
        """Initialize the phone search service."""
        self.adapter = ModuleAdapterService()
    
    def _parse_phone(self, phone: str) -> tuple[str, str]:
        """
        Parse phone number into country code and national number.
        
        Args:
            phone: Phone number string
            
        Returns:
            tuple[str, str]: (country_code, national_number)
            
        Raises:
            ValidationException: If phone number is invalid
        """
        try:
            # Add '+' if not present
            if not phone.startswith("+"):
                phone = "+" + phone
            
            phone_parse = phonenumbers.parse(phone, None)
            country_code = str(phone_parse.country_code)
            phone_no_country = str(phone_parse.national_number)
            
            logger.debug(f"Parsed phone: country={country_code}, number={phone_no_country}")
            return country_code, phone_no_country
        
        except phonenumbers.NumberParseException as e:
            logger.error(f"Invalid phone number: {phone} - {str(e)}")
            raise ValidationException(f"Invalid phone number format: {str(e)}")
    
    def _resolve_modules(self, requested_modules: list[str]) -> list[str]:
        """
        Resolve module list, expanding '*' to all active modules.
        
        Args:
            requested_modules: List of module names or ['*']
            
        Returns:
            list[str]: Resolved module names
        """
        if MODULE_ALL in requested_modules:
            return get_active_ignorant_modules()
        return list(set(requested_modules))
    
    def _validate_module(self, module_name: str, enforce_active: bool = True) -> None:
        """
        Validate that a module exists and is active.
        
        Args:
            module_name: Name of the module
            enforce_active: Whether to check if module is active
            
        Raises:
            ModuleNotFoundException: If module doesn't exist
            ModuleInactiveException: If module is not active
        """
        module_config = get_ignorant_module(module_name)
        
        if module_config is None:
            raise ModuleNotFoundException(module_name)
        
        if enforce_active and not module_config.active:
            raise ModuleInactiveException(module_name)
    
    async def _execute_module(
        self,
        module_name: str,
        phone_no_country: str,
        country_code: str,
        timeout: Optional[int] = None
    ) -> ModuleResult:
        """
        Execute a single module with DIRECT CONNECTIONS only.
        """
        from datetime import datetime, timezone
        try:
            # Validate module
            self._validate_module(module_name, enforce_active=True)
            
            # Get module configuration (WITH PROXY SETTINGS FILTERED)
            module_config = get_ignorant_module(module_name)
            module_func = module_config.func
            
            # Get client configuration (already filtered of proxy settings)
            client_config = module_config.client or {}
            from src.infrastructure.http.client import ModuleCompatibleClient
            # Create client with DIRECT CONNECTION only
            client = ModuleCompatibleClient(
                request_class=client_config.get("request_class"),
                impersonate=client_config.get("impersonate", "chrome99_android"),
                timeout=timeout or 10,
                #   NO PROXY SETTINGS PASSED
            )
            
            # Execute module
            output = []
            logger.info(f"Executing module with DIRECT CONNECTION: {module_name} for +{country_code}{phone_no_country}")
            
            await module_func(phone_no_country, country_code, client, output)
            
            # Adapt result
            records = self.adapter.adapt_ignorant_result(output)
            
            return ModuleResult(
                module_name=module_name,  #   ADDED module_name
                status=ResponseStatus.OK,
                code=HTTP_STATUS_OK,
                message="ok",
                records=records,
                timestamp= datetime.now(timezone.utc).replace(microsecond=0).isoformat()            )

        except NoDataFoundException:
            logger.info(f"No data found: {module_name}")
            return ModuleResult(
                module_name=module_name,  #   ADDED module_name
                status=ResponseStatus.OK,
                code=HTTP_STATUS_NO_CONTENT,
                message="No data found",
                records=[],
                timestamp= datetime.now(timezone.utc).replace(microsecond=0).isoformat()            )
        
        except RateLimitException as e:
            logger.warning(f"Rate limited: {module_name} - {str(e)}")
            return ModuleResult(
                module_name=module_name,  #   ADDED module_name
                status=ResponseStatus.ERROR,
                code=e.code,
                message=e.message,
                records=[],
                timestamp= datetime.now(timezone.utc).replace(microsecond=0).isoformat()            )
        
        except Exception as e:
            logger.error(f"Module execution failed: {module_name} - {str(e)}")
            return ModuleResult(
                module_name=module_name,  #   ADDED module_name
                status=ResponseStatus.ERROR,
                code=HTTP_STATUS_INTERNAL_ERROR,
                message=str(e),
                records=[],
                timestamp= datetime.now(timezone.utc).replace(microsecond=0).isoformat())
    
    async def search(
        self,
        request: PhoneSearchRequest,
        only_found: bool = False
    ) -> AggregatedResponse:  #   CHANGED return type
        """
        Perform phone search across multiple modules.
        
        Args:
            request: Phone search request
            only_found: If True, only return modules with found data
            
        Returns:
            AggregatedResponse: Aggregated results from all modules
        """
        logger.info(f"Starting phone search: {request.payload}")
        
        # Parse phone number
        country_code, phone_no_country = self._parse_phone(request.payload)
        
        # Resolve modules
        modules = self._resolve_modules(request.modules)
        logger.info(f"Executing {len(modules)} modules")
        
        # Execute all modules concurrently
        tasks = [
            self._execute_module(module, phone_no_country, country_code, request.timeout)
            for module in modules
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=False)
        
        # Build results dictionary
        results_dict = {}
        successful = 0
        failed = 0
        
        for result in results:
            # Filter if only_found is True
            if only_found and result.code == HTTP_STATUS_NO_CONTENT:
                continue
            
            results_dict[result.module_name] = result
            
            if result.status == ResponseStatus.OK:
                successful += 1
            else:
                failed += 1
        
        logger.info(
            f"Search completed: {len(results_dict)} results "
            f"({successful} successful, {failed} failed)"
        )
        from datetime import datetime, timezone

        return AggregatedResponse(  #   CHANGED to AggregatedResponse
            total_modules=len(modules),
            successful=successful,
            failed=failed,
            results=results_dict,
            timestamp= datetime.now(timezone.utc).replace(microsecond=0).isoformat()        )
    
    def get_all_modules(self) -> list[str]:
        """Get list of all phone modules."""
        return get_all_ignorant_modules()
    
    def get_active_modules(self) -> list[str]:
        """Get list of active phone modules."""
        return get_active_ignorant_modules()