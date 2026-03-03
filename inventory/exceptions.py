from rest_framework.exceptions import APIException
from rest_framework import status

class CompanyNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, company_key):
        detail = {
            "title": "Company not found",
            "description": f"The company with company key {company_key} was not found"
        }
        super().__init__(detail)