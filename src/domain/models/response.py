from datetime import datetime, timezone
from typing import Any, Optional, List, Dict
from pydantic import BaseModel, Field

from src.core.constants import ResponseStatus, ResultCode, DataType


class ResponseHeaders(BaseModel):
    """Response headers with service identification."""
    sender: str = Field(..., description="Service name that generated the response")


class StandardResponse(BaseModel):
    """Standard response format according to Sfera guidelines."""
    headers: ResponseHeaders = Field(..., description="Response metadata")
    body: dict[str, Any] = Field(..., description="Main logical information from service")
    extra: dict[str, Any] = Field(default_factory=dict, description="Additional information")


# ===== LEGACY COMPATIBILITY MODELS (Internal use only) =====

class DataRecord(BaseModel):
    """Individual data record in search results."""
    result: str = Field(..., description="Result description")
    result_code: ResultCode = Field(..., description="Result code")
    phone_number: Optional[str] = Field(None, description="Associated phone number")
    email_recovery: Optional[str] = Field(None, description="Recovery email")
    
    class Config:
        use_enum_values = True


class ModuleResult(BaseModel):
    """Result from a single module."""
    module_name: str = Field(..., description="Name of the module")
    status: ResponseStatus = Field(..., description="Module execution status")
    code: int = Field(..., description="Result code")
    message: str = Field(..., description="Result message")
    records: list[DataRecord] = Field(default_factory=list, description="Found records")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).replace(microsecond=0).isoformat())
    
    class Config:
        use_enum_values = True


class AggregatedResponse(BaseModel):
    """Aggregated response for internal processing."""
    total_modules: int = Field(..., description="Total number of modules executed")
    successful: int = Field(..., description="Number of successful modules")
    failed: int = Field(..., description="Number of failed modules")
    results: dict[str, ModuleResult] = Field(..., description="Results by module name")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).replace(microsecond=0).isoformat())


# ===== SFERA-COMPLIANT RESPONSE MODELS =====

class ModuleListResponse(StandardResponse):
    """Sfera-compliant module list response."""


class SearchResponse(StandardResponse):
    """Sfera-compliant search response."""


class OrchestratorResponse(StandardResponse):
    """Sfera-compliant orchestrator response."""


class HealthResponse(StandardResponse):
    """Sfera-compliant health check response."""