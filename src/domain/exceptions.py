
from typing import Optional


class DomainException(Exception):
    """Base exception for domain layer."""
    
    def __init__(self, message: str, code: int = 500):
        self.message = message
        self.code = code
        super().__init__(self.message)


class ValidationException(DomainException):
    """Raised when input validation fails."""
    
    def __init__(self, message: str = "Invalid input data"):
        super().__init__(message, code=400)


class ModuleNotFoundException(DomainException):
    """Raised when a requested module is not found."""
    
    def __init__(self, module_name: str):
        super().__init__(f"Module '{module_name}' not found", code=404)


class ModuleInactiveException(DomainException):
    """Raised when trying to use an inactive module."""
    
    def __init__(self, module_name: str):
        super().__init__(f"Module '{module_name}' is not active", code=400)


class NoDataFoundException(DomainException):
    """Raised when no data is found for the query."""
    
    def __init__(self, message: str = "No data found"):
        super().__init__(message, code=204)


class RateLimitException(DomainException):
    """Raised when rate limit is exceeded."""
    
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, code=429)


class ModuleExecutionException(DomainException):
    """Raised when module execution fails."""
    
    def __init__(self, module_name: str, reason: Optional[str] = None):
        message = f"Module '{module_name}' execution failed"
        if reason:
            message += f": {reason}"
        super().__init__(message, code=500)


class TimeoutException(DomainException):
    """Raised when operation times out."""
    
    def __init__(self, message: str = "Operation timed out"):
        super().__init__(message, code=504)


class ExternalServiceException(DomainException):
    """Raised when external service call fails."""
    
    def __init__(self, service_name: str, reason: Optional[str] = None):
        message = f"External service '{service_name}' failed"
        if reason:
            message += f": {reason}"
        super().__init__(message, code=503)