import asyncio
from typing import Optional
from datetime import datetime, timezone

from src.core.constants import (
    ResponseStatus, MODULE_ALL, HTTP_STATUS_OK,
    HTTP_STATUS_NO_CONTENT, HTTP_STATUS_INTERNAL_ERROR
)
from src.core.logging import get_logger
from src.domain.exceptions import (
    ModuleNotFoundException, ModuleInactiveException,
    NoDataFoundException, RateLimitException, ModuleExecutionException
)
from src.domain.models.search import EmailSearchRequest
from src.domain.models.response import ModuleResult, AggregatedResponse, DataRecord
from src.domain.services.module_adapter_service import ModuleAdapterService
from src.infrastructure.modules.holehe_modules import (
    get_holehe_module, get_active_holehe_modules, get_all_holehe_modules
)

logger = get_logger(__name__)

class EmailSearchService:
    """Service for performing email searches with legacy-compatible logic."""
    
    def __init__(self):
        self.adapter = ModuleAdapterService()
    
    def _resolve_modules(self, requested_modules: list[str]) -> list[str]:
        """Resolve module list with legacy logic."""
        if MODULE_ALL in requested_modules:
            return get_active_holehe_modules()
        return list(set(requested_modules))
    
    def _validate_module(self, module_name: str, enforce_active: bool = True) -> None:
        """Validate module with legacy enforcement."""
        module_config = get_holehe_module(module_name)
        
        if module_config is None:
            raise ModuleNotFoundException(module_name)
        
        #   ENFORCE ACTIVE FLAG (was commented in legacy)
        if enforce_active and not module_config.active:
            raise ModuleInactiveException(module_name)
    
    async def _execute_module(
        self,
        module_name: str,
        email: str,
        timeout: Optional[int] = None
    ) -> ModuleResult:
        """
        Execute single module with legacy-compatible error handling.
        USES FILTERED CONFIGURATIONS (no proxy).
        """
        try:
            # Validate module (now enforces active flag)
            self._validate_module(module_name, enforce_active=True)
            
            # Get module configuration (WITH PROXY SETTINGS FILTERED)
            module_config = get_holehe_module(module_name)
            module_func = module_config.func
            
            # Get client configuration (already filtered of proxy settings)
            client_config = module_config.client or {}
            
            # Create client with DIRECT CONNECTION only
            from src.infrastructure.http.client import ModuleCompatibleClient
            client = ModuleCompatibleClient(
                request_class=client_config.get("request_class"),
                impersonate=client_config.get("impersonate", "chrome99_android"),
                timeout=timeout or 10,
                #   NO PROXY SETTINGS PASSED - they're filtered at module level
            )
            
            # Execute module (legacy pattern preserved exactly)
            output = []
            logger.info(f"Executing module with DIRECT CONNECTION: {module_name} for {email}")
            
            await module_func(email, client, output)  #   EXACT LEGACY PATTERN
            
            # Adapt result using legacy business logic
            records = self.adapter.adapt_holehe_result(output)
            
            return ModuleResult(
                module_name=module_name,  #   ADDED module_name
                status=ResponseStatus.OK,
                code=HTTP_STATUS_OK,
                message="ok",
                records=records,
                timestamp= datetime.now(timezone.utc).replace(microsecond=0).isoformat()            )
        
        except NoDataFoundException:
            logger.info(f"No data found: {module_name}")
            # Legacy-compatible no data response
            return ModuleResult(
                module_name=module_name,  #   ADDED module_name
                status=ResponseStatus.OK,  # Note: OK status for no data (legacy behavior)
                code=HTTP_STATUS_NO_CONTENT,
                message="No data found",
                records=[],
                timestamp= datetime.now(timezone.utc).replace(microsecond=0).isoformat()            )
        
        except RateLimitException as e:
            logger.warning(f"Rate limited: {module_name} - {str(e)}")
            # Legacy-compatible rate limit response
            return ModuleResult(
                module_name=module_name,  #   ADDED module_name
                status=ResponseStatus.ERROR,
                code=429,  # 429 Too Many Requests
                message=str(e),
                records=[],
                timestamp= datetime.now(timezone.utc).replace(microsecond=0).isoformat()            )
        
        except Exception as e:
            logger.error(f"Module execution failed: {module_name} - {str(e)}")
            # Legacy-compatible error response
            error_code = getattr(e, 'code', HTTP_STATUS_INTERNAL_ERROR)
            return ModuleResult(
                module_name=module_name,  #   ADDED module_name
                status=ResponseStatus.ERROR,
                code=error_code,
                message=str(e),
                records=[],
                timestamp= datetime.now(timezone.utc).replace(microsecond=0).isoformat()            )
    
    async def search(
        self,
        request: EmailSearchRequest,
        only_found: bool = False
    ) -> AggregatedResponse:  #   CHANGED return type
        """
        Perform email search with legacy-compatible aggregation.
        """
        logger.info(f"Starting email search: {request.payload}")
        
        # Resolve modules
        modules = self._resolve_modules(request.modules)
        logger.info(f"Executing {len(modules)} modules")
        
        # Execute all modules concurrently (legacy pattern)
        tasks = [
            self._execute_module(module, request.payload, request.timeout)
            for module in modules
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=False)
        
        # Build results with legacy filtering
        results_dict = {}
        successful = 0
        failed = 0
        
        for result in results:
            # Legacy "only_found" filtering
            if only_found and result.code == HTTP_STATUS_NO_CONTENT:
                continue
            
            results_dict[result.module_name] = result
            
            if result.status == ResponseStatus.OK and result.code != HTTP_STATUS_NO_CONTENT:
                successful += 1
            else:
                failed += 1
        
        logger.info(
            f"Search completed: {len(results_dict)} results "
            f"({successful} successful, {failed} failed)"
        )
        
        return AggregatedResponse(  #   CHANGED to AggregatedResponse
            total_modules=len(modules),
            successful=successful,
            failed=failed,
            results=results_dict,
            timestamp= datetime.now(timezone.utc).replace(microsecond=0).isoformat()        )
    
    def get_all_modules(self) -> list[str]:
        return get_all_holehe_modules()
    
    def get_active_modules(self) -> list[str]:
        return get_active_holehe_modules()