from django.urls import path
from apps.company.views import CompanyCreateView, CompanyRetrieveUpdateView

urlpatterns = [
    path("", CompanyCreateView.as_view(), name="company-create"),
    path("/<uuid:company_key>", CompanyRetrieveUpdateView.as_view(), name="company-retrieve-update"),
]