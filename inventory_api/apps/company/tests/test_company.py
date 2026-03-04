import pytest
from rest_framework.test import APIClient
from common.utils import Mock
from pathlib import Path
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIRECTORY = Path(__file__).resolve().parent
INTERNAL_API_TOKEN = os.getenv("INTERNAL_API_TOKEN")

@pytest.fixture
def client():
    return APIClient()

@pytest.mark.django_db
class TestCompany:
    def test_company_happy_flow(self, client):
        
        company_payload = Mock.load_payload(f'{BASE_DIRECTORY}/payloads/create_company.json')
        response = client.post('/inventory/company', company_payload, format='json', headers={"X-INTERNAL-TOKEN": INTERNAL_API_TOKEN})
        assert response.status_code == 201
        response_data = response.data
        assert response_data['company_key'] is not None

        company_key = response_data['company_key']

        response = client.get(f'/inventory/company/{company_key}', headers={"X-INTERNAL-TOKEN": INTERNAL_API_TOKEN})

        assert response.status_code == 200
        response_data = response.data
        assert response_data['name'] == company_payload['name']
        assert response_data['company_data'] == company_payload['company_data']
        assert response_data['status'] == "active"
        
        update_company_payload = company_payload
        update_company_payload['name'] = "Marvel Corporation"
        update_company_payload['company_data']['email'] = "admin@marvel.com"
        response = client.patch(f'/inventory/company/{company_key}', update_company_payload, headers={"X-INTERNAL-TOKEN": INTERNAL_API_TOKEN}, format='json')

        assert response.status_code == 200
        response_data = response.data
        assert response_data['name'] == update_company_payload['name']
        assert response_data['company_data'] == update_company_payload['company_data']
        assert response_data['status'] == "active"
        
    def test_company_invalid_payload(self, client):

        company_payload = Mock.load_payload(f'{BASE_DIRECTORY}/payloads/create_company.json')
        del company_payload['name']

        response = client.post('/inventory/company', company_payload, headers={"X-INTERNAL-TOKEN": INTERNAL_API_TOKEN}, format='json')
        assert response.status_code == 400 

    def test_company_not_found(self, client):
        
        company_payload = Mock.load_payload(f'{BASE_DIRECTORY}/payloads/create_company.json')
        random_company_key = str(uuid.uuid4())

        response = client.get(f'/inventory/company/{random_company_key}', headers={"X-INTERNAL-TOKEN": INTERNAL_API_TOKEN})
        assert response.status_code == 404
        response_data = response.data
        assert response_data['title'] == "Company not found"
        assert response_data['description'] == f"The company with company key {random_company_key} was not found"

        response = client.patch(f'/inventory/company/{random_company_key}', company_payload, headers={"X-INTERNAL-TOKEN": INTERNAL_API_TOKEN}, format='json')
        assert response.status_code == 404
        response_data = response.data
        assert response_data['title'] == "Company not found"
        assert response_data['description'] == f"The company with company key {random_company_key} was not found"

    
    