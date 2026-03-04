from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Company
from .serializers import CompanyCreateSerializer, CompanyCreateResponseSerializer, CompanyRetrieveResponseSerializer, CompanyUpdateSerializer
from common.exceptions import CompanyNotFound
from common.permissions import InternalRequest
import logging

logger = logging.getLogger(__name__)

class CompanyCreateView(APIView):

    permission_classes = [InternalRequest] 

    def post(self, request):
        logger.info("Request on Company Creation")

        serializer = CompanyCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company = serializer.save()
        response_serializer = CompanyCreateResponseSerializer(company)
        return Response(response_serializer.data, status=201)
    
class CompanyRetrieveUpdateView(APIView):

    permission_classes = [InternalRequest] 

    def get(self, request, company_key):
        logger.info(f"Retrieve company with company key {company_key}")

        try:
            company = Company.objects.get(company_key=company_key)
        except Company.DoesNotExist:
            raise CompanyNotFound(company_key)

        company_serializer = CompanyRetrieveResponseSerializer(company)
        return Response(company_serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, company_key):
        logger.info(f"Updating company with company key {company_key}")

        try:
            company = Company.objects.get(company_key=company_key)
        except Company.DoesNotExist:
            raise CompanyNotFound(company_key)

        company_serializer = CompanyUpdateSerializer(
            company,
            data=request.data,
            partial=True
        )

        company_serializer.is_valid(raise_exception=True)
        company = company_serializer.save()
    
        return Response(company_serializer.data, status=status.HTTP_200_OK)



        