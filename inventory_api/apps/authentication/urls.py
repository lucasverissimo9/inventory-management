from django.urls import path
from apps.authentication import views

urlpatterns = [
    path("/register", views.AuthRegisterView.as_view(), name="auth-register"),
    path("/login", views.AuthLoginView.as_view(), name="auth-login"),
    path("/logout", views.AuthLogoutView.as_view(), name="auth-logout"),
]