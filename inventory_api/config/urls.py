from django.urls import path, include

urlpatterns = [
    path("inventory/", include("config.routes")),
]