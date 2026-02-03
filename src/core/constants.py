

from enum import Enum


class DataType(str, Enum):
    """Types of data that can be searched."""
    EMAIL = "email"
    PHONE = "phone"
    UNKNOWN = "unknown"


class ResultCode(str, Enum):
    """Result codes for search operations."""
    FOUND = "FOUND"
    NOT_FOUND = "NOT_FOUND"
    MATCHED = "MATCHED"
    ERROR = "ERROR"
    RATE_LIMITED = "RATE_LIMITED"
    TIMEOUT = "TIMEOUT"


class ResponseStatus(str, Enum):
    """Response status values."""
    OK = "ok"
    ERROR = "error"


# HTTP Status Codes
HTTP_STATUS_OK = 200
HTTP_STATUS_NO_CONTENT = 204
HTTP_STATUS_BAD_REQUEST = 400
HTTP_STATUS_NOT_FOUND = 404
HTTP_STATUS_INTERNAL_ERROR = 500
HTTP_STATUS_SERVICE_UNAVAILABLE = 503

# Module Constants
MODULE_ALL = "*"
DEFAULT_MODULE_TIMEOUT = 10  # seconds

# Validation Messages
MSG_FOUND = "Найден"
MSG_NOT_FOUND = "Не найден"
MSG_RATE_LIMITED = "Превышен лимит запросов"
MSG_INTERNAL_ERROR = "Внутренняя ошибка модуля"
MSG_TIMEOUT = "Превышено время ожидания"
MSG_INVALID_INPUT = "Некорректные входные данные"