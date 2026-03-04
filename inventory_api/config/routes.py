from django.urls import path, include

urlpatterns = [
    path("company", include("apps.company.urls")),
    path("company/<uuid:company_key>/", include([
        path("auth", include("apps.authentication.urls"))
    ])),
]