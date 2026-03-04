from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from apps.authentication.serializers import AuthLoginSerializer, AuthRegisterSerializer
from apps.company.models import Company
from apps.users.serializers import UserSerializer
from common.exceptions import CompanyNotFound

def _set_refresh_cookie(response, token):
    response.set_cookie(
        key=settings.JWT_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=settings.JWT_COOKIE_SECURE,
        samesite="Strict",
        max_age=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()),
        path="/api/auth/",
    )

def _auth_response(user, status_code):
    refresh = RefreshToken.for_user(user)
    response = Response(
        {"access_token": str(refresh.access_token), "user": UserSerializer(user).data},
        status=status_code,
    )
    _set_refresh_cookie(response, str(refresh))
    return response


def _get_company_or_404(company_key):
    try:
        return Company.objects.get(company_key=company_key, status="active")
    except Company.DoesNotExist:
        raise CompanyNotFound(company_key)

class AuthLoginView(APIView):
    permission_classes = [AllowAny]
    throttle_scope = "auth"

    def post(self, request, company_key):
        company = _get_company_or_404(company_key=company_key)
        serializer = AuthLoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        return _auth_response(user)


class AuthRegisterView(APIView):
    permission_classes = [AllowAny]
    throttle_scope = "auth"

    def post(self, request, company_key):
        company = _get_company_or_404(company_key)
        serializer = AuthRegisterSerializer(
            data=request.data,
            context={"company": company}, 
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return _auth_response(user, status.HTTP_201_CREATED)

class AuthLogoutView(APIView):
    def post(self, request, company_key):
        token = request.COOKIES.get(settings.JWT_COOKIE_NAME)
        if token:
            try:
                RefreshToken(token).blacklist()
            except TokenError:
                pass
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie(settings.JWT_COOKIE_NAME, path="/api/auth/")
        return response

