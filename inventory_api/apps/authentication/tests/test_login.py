import pytest
from rest_framework.test import APIClient
from apps.authentication.tests.factories import UserFactory, CompanyFactory

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user(db):
    return UserFactory()

@pytest.fixture
def company(db):
    return CompanyFactory()

@pytest.mark.django_db
class TestLoginView:

    def test_access_token(self, client, company, user):
        user_information = {"email": str(user.email), "password": "password123"}
        response = client.post(f"/inventory/company/{company.company_key}/auth/login", user_information, format='json')
        assert response.status_code == 200
        response_data = response.data
        assert response_data["access_token"] is not None
        assert response_data["user"]["email"] == user.email

    def test_invalid_password(self, client, company, user):
        user_information = {"email": str(user.email), "password": "potato123"}
        response = client.post(f"/inventory/company/{company.company_key}/auth/login", user_information, format='json')
        assert response.status_code == 400
        response_data = response.data
        assert response_data["title"] == "Invalid Data"
        assert response_data["description"] == "Invalid Data on User Login"

    def test_refresh_cookie_http_only(self, client, company, user):
        user_information = {"email": str(user.email), "password": "password123"}

        response = client.post(f"/inventory/company/{company.company_key}/auth/login", user_information, format='json')
        assert response.status_code == 200
        cookie = response.cookies.get("refresh_token")
        assert cookie is not None
        assert cookie["httponly"] is True

    def test_login_with_inactive_user(self, client, company, user):
        user.status="active"
        user.save()
        
        user_information = {"email": str(user.email), "password": "password123"}
        response = client.post(f"/inventory/company/{company.company_key}/auth/login", user_information, format='json')
        assert response.status_code == 400
        response_data = response.data
        assert response_data['title'] == "Inactivated User"
        assert response_data['description'] == "The user is inactive"

