from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
import logging

logger = logging.getLogger(__name__)

def client_exception_handler(exc, context):
    
    if isinstance(exc, DjangoValidationError):
        from rest_framework.exceptions import ValidationError
        exc = ValidationError(exc.messages)

    response = exception_handler(exc, context)

    if response is None:
        return Response(
            {"title": "Server Error", "message": "Unexpected error."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response


class CompanyNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, company_key):
        exception = {
            "title": "Company not found",
            "description": f"The company with company key {company_key} was not found"
        }
        super().__init__(exception)


class UserEmailNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, email):
        exception = {
            "title": "User not found",
            "description": f"The user with email {email} was not found"
        }
        super().__init__(exception)