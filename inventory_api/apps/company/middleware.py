from django.utils.functional import SimpleLazyObject
from apps.company.models import CompanyUserMembership


def _verify_request_company(request):
    company_key = request.headers.get("X-COMPANY-IDENTIFIER")

    if not company_key or not request.user.is_authenticated:
        return None

    try:
        user_membership = CompanyUserMembership.objects.select_related("company").get(
            user=request.user,
            company_key=company_key,
            status="active",
        )
        return user_membership.company
    except CompanyUserMembership.DoesNotExist:
        return None


class CompanyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.company = SimpleLazyObject(_verify_request_company(request))
        return self.get_response(request)