from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)


class BaseAPIException(Exception):
    """
    Base exception class for API-related errors.
    """
    default_message = "An error occurred"
    default_code = "error"
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, message=None, code=None, status_code=None):
        self.message = message or self.default_message
        self.code = code or self.default_code
        if status_code:
            self.status_code = status_code
        super().__init__(self.message)


class ValidationError(BaseAPIException):
    """
    Exception for validation errors.
    """
    default_message = "Validation failed"
    default_code = "validation_error"
    status_code = status.HTTP_400_BAD_REQUEST


class NotFoundError(BaseAPIException):
    """
    Exception for resource not found errors.
    """
    default_message = "Resource not found"
    default_code = "not_found"
    status_code = status.HTTP_404_NOT_FOUND


class PermissionError(BaseAPIException):
    """
    Exception for permission denied errors.
    """
    default_message = "Permission denied"
    default_code = "permission_denied"
    status_code = status.HTTP_403_FORBIDDEN


class BusinessLogicError(BaseAPIException):
    """
    Exception for business logic violations.
    """
    default_message = "Business logic error"
    default_code = "business_logic_error"
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY


def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides consistent error responses.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        # Log the exception
        logger.error(f"API Exception: {exc}", exc_info=True)
        
        # Customize the response format
        custom_response_data = {
            'error': {
                'message': str(exc),
                'code': getattr(exc, 'code', 'error'),
                'status_code': response.status_code,
                'details': response.data if hasattr(response, 'data') else None
            }
        }
        response.data = custom_response_data

    elif isinstance(exc, BaseAPIException):
        # Handle our custom exceptions
        logger.error(f"Custom API Exception: {exc}", exc_info=True)
        
        response = Response(
            {
                'error': {
                    'message': exc.message,
                    'code': exc.code,
                    'status_code': exc.status_code
                }
            },
            status=exc.status_code
        )

    return response
