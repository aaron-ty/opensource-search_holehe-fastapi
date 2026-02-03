from datetime import datetime, timezone
from typing import Any, Optional, List
from pydantic import BaseModel, Field

from src.core.constants import DataType
from src.domain.models.response import StandardResponse, ResponseHeaders


class OrchestratorRequest(BaseModel):
    """Request for the orchestrator controller with validator."""
    queries: list[str] = Field(..., description="List of queries to process (emails, phones, etc.)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "queries": ["example@gmail.com", "79319999999"]
            }
        }


class DirectSearchRequest(BaseModel):
    """Request for direct search without validator."""
    queries: list[str] = Field(..., description="List of queries to process")
    
    class Config:
        json_schema_extra = {
            "example": {
                "queries": ["test@example.com", "+79123456789"]
            }
        }


class ValidatedQuery(BaseModel):
    """Validated query with detected type."""
    original: str = Field(..., description="Original query string")
    clean: str = Field(..., description="Cleaned/normalized query")
    data_type: DataType = Field(..., description="Detected data type")
    extra_data: dict[str, Any] = Field(default_factory=dict, description="Additional validation data")
    
    class Config:
        use_enum_values = True


class OrchestratorResponse(BaseModel):
    """Sfera-compliant orchestrator response."""
    headers: ResponseHeaders = Field(..., description="Response headers")
    body: dict[str, Any] = Field(..., description="Orchestrator result data")
    extra: dict[str, Any] = Field(default_factory=dict, description="Additional information")
    
    class Config:
        from src.core.config import get_settings
        settings = get_settings()

        json_schema_extra = {
            "example": {
                "headers": {"sender": f"{settings.APP_NAME} - sfera.orchestrator"},
                "body": {
                    "total_queries": 2,
                    "processed_queries": 2,
                    "results": [
                        {
                            "headers": {"sender": f"{settings.APP_NAME} - sfera.email.gravatar"},
                            "body": {
                                "query": "example@gmail.com",
                                "module": "gravatar",
                                "status": "ok",
                                "found": True,
                                "records": [
                                    {
                                        "result": "Найден",
                                        "result_code": "FOUND"
                                    }
                                ]
                            },
                            "extra": {
                                "timestamp": "2025-11-20T13:15:33+00:00",
                                "data_type": "email"
                            }
                        }
                    ]
                },
                "extra": {
                    "timestamp": "2025-11-20T13:15:33+00:00",
                    "validation_source": "validator"
                }
            }
        }