import asyncio
from typing import List
from src.core.config import get_settings
from src.core.constants import DataType
from src.core.logging import get_logger
from src.domain.models.orchestrator import (
    OrchestratorRequest, 
    OrchestratorResponse, 
    ValidatedQuery,
    DirectSearchRequest
)
from src.domain.models.response import StandardResponse, ResponseHeaders
from src.domain.models.search import EmailSearchRequest, PhoneSearchRequest
from src.controllers.email_controller import EmailController
from src.controllers.phone_controller import PhoneController
from src.infrastructure.validators.validator_client import ValidatorClient

logger = get_logger(__name__)

class OrchestratorController:
    """Enhanced orchestrator with Sfera-compliant responses."""
    
    def __init__(self):
        self.email_controller = EmailController()
        self.phone_controller = PhoneController()
        self.settings = get_settings()
        self.service_name = f"{self.settings.APP_NAME} - sfera.orchestrator"
        
        # Initialize validator with fallback support
        self.validator_client = ValidatorClient(
            self.settings.VALIDATOR_URL if self.settings.VALIDATOR_ENABLED else None
        )
    
    async def process_with_validator(self, request: OrchestratorRequest) -> OrchestratorResponse:
        """Process queries using validator service with Sfera-compliant response."""
        logger.info(f"Orchestrator processing {len(request.queries)} queries with validator")
        
        # Validate all queries
        validation_tasks = [
            self._validate_with_fallback(query)
            for query in request.queries
        ]
        validated_queries = await asyncio.gather(*validation_tasks, return_exceptions=True)
        
        # Process validated queries
        processing_tasks = []
        for i, validated in enumerate(validated_queries):
            if isinstance(validated, Exception):
                logger.error(f"Validation failed for query {request.queries[i]}: {str(validated)}")
                # Create error response for failed validation
                processing_tasks.append(self._create_error_response(request.queries[i], str(validated)))
                continue
            processing_tasks.append(self._process_single_query(validated))
        
        results_lists = await asyncio.gather(*processing_tasks, return_exceptions=True)
        
        # Flatten results
        all_results = []
        for results in results_lists:
            if isinstance(results, Exception):
                logger.error(f"Processing failed: {str(results)}")
                continue
            all_results.extend(results)
        
        logger.info(f"Orchestrator completed: {len(all_results)} total results")
        from datetime import datetime, timezone

        return OrchestratorResponse(
            headers=ResponseHeaders(sender=self.service_name),
            body={
                "total_queries": len(request.queries),
                "processed_queries": len(all_results),
                "successful_queries": len([r for r in all_results if r.body.get("status") == "ok"]),
                "failed_queries": len([r for r in all_results if r.body.get("status") == "error"]),
                "results": [result.dict() for result in all_results]
            },
            extra={
                "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
                "validation_source": "validator",
                "service_version": self.settings.APP_VERSION
            }
        )
    
    async def process_direct(self, request: DirectSearchRequest) -> OrchestratorResponse:
        """Process queries using direct validation only with Sfera-compliant response."""
        logger.info(f"Direct orchestrator processing {len(request.queries)} queries")
        
        # Use direct validation only
        validation_tasks = [
            self.validator_client.validate_direct_only(query)
            for query in request.queries
        ]
        validation_results = await asyncio.gather(*validation_tasks)
        
        # Process queries
        processing_tasks = []
        for i, validation_result in enumerate(validation_results):
            validated = ValidatedQuery(
                original=request.queries[i],
                clean=validation_result.get("clean_data", request.queries[i]),
                data_type=DataType(validation_result.get("type", "unknown")),
                extra_data=validation_result.get("extra", {})
            )
            processing_tasks.append(self._process_single_query(validated))
        
        results_lists = await asyncio.gather(*processing_tasks, return_exceptions=True)
        
        # Flatten results
        all_results = []
        for results in results_lists:
            if isinstance(results, Exception):
                logger.error(f"Processing failed: {str(results)}")
                continue
            all_results.extend(results)
        
        logger.info(f"Direct orchestrator completed: {len(all_results)} total results")
        from datetime import datetime, timezone

        return OrchestratorResponse(
            headers=ResponseHeaders(sender=self.service_name),
            body={
                "total_queries": len(request.queries),
                "processed_queries": len(all_results),
                "successful_queries": len([r for r in all_results if r.body.get("status") == "ok"]),
                "failed_queries": len([r for r in all_results if r.body.get("status") == "error"]),
                "results": [result.dict() for result in all_results]
            },
            extra={
                "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
                "validation_source": "direct",
                "service_version": self.settings.APP_VERSION
            }
        )
    
    async def _validate_with_fallback(self, query: str) -> ValidatedQuery:
        """Validate query with guaranteed fallback."""
        
        try:
            if self.settings.VALIDATOR_ENABLED and self.validator_client.base_url:
                validation_result = await self.validator_client.validate(query)
            else:
                validation_result = await self.validator_client.validate_direct_only(query)
                
            return ValidatedQuery(
                original=query,
                clean=validation_result.get("clean_data", query),
                data_type=DataType(validation_result.get("type", "unknown")),
                extra_data=validation_result.get("extra", {})
            )
        except Exception as e:
            logger.warning(f"Validation failed, using direct: {str(e)}")
            # Direct fallback
            validation_result = await self.validator_client.validate_direct_only(query)
            return ValidatedQuery(
                original=query,
                clean=validation_result.get("clean_data", query),
                data_type=DataType(validation_result.get("type", "unknown")),
                extra_data=validation_result.get("extra", {})
            )
    
    async def _process_single_query(self, validated: ValidatedQuery) -> list[StandardResponse]:
        """Process single query with proper error handling."""
        logger.info(f"Processing {validated.data_type} query: {validated.clean}")

        try:
            if validated.data_type == DataType.EMAIL:
                return await self.email_controller.search_as_standard_response(
                    email=validated.clean,
                    modules=["*"]
                )
            elif validated.data_type == DataType.PHONE:
                return await self.phone_controller.search_as_standard_response(
                    phone=validated.clean,
                    modules=["*"]
                )
            else:
                logger.warning(f"Unsupported data type for query: {validated.original}")
                return [self._create_error_response(
                    validated.original, 
                    f"Unsupported data type: {validated.data_type}"
                )]
        except Exception as e:
            logger.error(f"Error processing query {validated.clean}: {str(e)}")
            return [self._create_error_response(validated.original, f"Processing failed: {str(e)}")]
    
    def _create_error_response(self, query: str, error_message: str) -> StandardResponse:
        """Create error response in Sfera format."""
        from datetime import datetime, timezone

        return StandardResponse(
            headers=ResponseHeaders(sender=self.service_name),
            body={
                "query": query,
                "error": error_message,
                "status": "error",
                "code": 500
            },
            extra={
                "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
                "supported_types": ["email", "phone"]
            }
        )
    
    async def search_email_direct(self, email: str, modules: list[str]) -> OrchestratorResponse:
        """Direct email search with Sfera-compliant response."""
        try:
            results = await self.email_controller.search_as_standard_response(email, modules)
            from datetime import datetime, timezone

            return OrchestratorResponse(
                headers=ResponseHeaders(sender=self.service_name),
                body={
                    "query": email,
                    "total_results": len(results),
                    "results": [result.dict() for result in results],
                    "data_type": "email"
                },
                extra={
                    "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
                    "validation_source": "direct",
                    "modules_used": modules
                }
            )
        except Exception as e:
            logger.error(f"Direct email search failed: {str(e)}")
            return self._create_orchestrator_error_response(str(e))
    
    async def search_phone_direct(self, phone: str, modules: list[str]) -> OrchestratorResponse:
        """Direct phone search with Sfera-compliant response."""
        try:
            results = await self.phone_controller.search_as_standard_response(phone, modules)
            from datetime import datetime, timezone

            return OrchestratorResponse(
                headers=ResponseHeaders(sender=self.service_name),
                body={
                    "query": phone,
                    "total_results": len(results),
                    "results": [result.dict() for result in results],
                    "data_type": "phone"
                },
                extra={
                    "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
                    "validation_source": "direct",
                    "modules_used": modules
                }
            )
        except Exception as e:
            logger.error(f"Direct phone search failed: {str(e)}")
            return self._create_orchestrator_error_response(str(e))
    
    def _create_orchestrator_error_response(self, error_message: str) -> OrchestratorResponse:
        """Create orchestrator error response in Sfera format."""
        from datetime import datetime, timezone

        return OrchestratorResponse(
            headers=ResponseHeaders(sender=self.service_name),
            body={
                "error": error_message,
                "status": "error",
                "code": 500
            },
            extra={
                "timestamp":  datetime.now(timezone.utc).replace(microsecond=0).isoformat()            }
        )