from rest_framework.permissions import BasePermission
from apps.company.models import CompanyUserMembership


class VerifyCompanyMember(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.company is not None


class VerifyCompanyAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated or not request.company:
            return False
        return CompanyUserMembership.objects.filter(
            user=request.user,
            company=request.company,
            user_role__in=[CompanyUserMembership.Role.OWNER, CompanyUserMembership.Role.ADMIN],
        ).exists()