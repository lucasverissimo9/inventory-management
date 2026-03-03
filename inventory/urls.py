
from django.urls import path
from .views import CompanyCreateView, CompanyRetrieveUpdateView

urlpatterns = [
    path("inventory/company", view=CompanyCreateView.as_view(), name="company-create-view"),
    path("inventory/company/<uuid:company_key>", view=CompanyRetrieveUpdateView.as_view(), name="company-retrieve-view")
]
