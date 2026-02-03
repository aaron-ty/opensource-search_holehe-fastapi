from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    """Base search request model."""
    payload: str = Field(..., description="Email or phone number to search")
    modules: list[str] = Field(default=["*"], description="List of modules to use (* for all active)")
    timeout: Optional[int] = Field(default=None, description="Maximum execution time in seconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "payload": "example@gmail.com",
                "modules": ["gravatar", "adobe"]
            }
        }


class EmailSearchRequest(SearchRequest):
    """Email search request model."""
    
    class Config:
        json_schema_extra = {
            "example": {
                "payload": "example@gmail.com",
                "modules": ["*"]
            }
        }


class PhoneSearchRequest(SearchRequest):
    """Phone search request model."""
    
    class Config:
        json_schema_extra = {
            "example": {
                "payload": "79319999999",
                "modules": ["instagram", "snapchat"]
            }
        }