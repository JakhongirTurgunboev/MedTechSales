import datetime

import pytest
from rest_framework.test import APIClient
from django.urls import reverse

from app.models import Employee, Client


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_employee_statistics(api_client):
    # Create test data (adjust as needed)
    employee = Employee.objects.create(full_name='test_employee', birth_date=datetime.date.today())
    url = reverse('employee-statistics', kwargs={'id': employee.id})

    # Make a request to the view
    response = api_client.get(url)

    # Assert the response status code and content
    assert response.status_code == 200
    assert 'employee_name' in response.data
    assert 'number_of_clients' in response.data
    assert 'number_of_products' in response.data
    assert 'sum_of_sales' in response.data


@pytest.mark.django_db
def test_employee_statistics_summary(api_client):
    url = reverse('employee-statistics-summary')

    # Make a request to the view
    response = api_client.get(url)

    # Assert the response status code and content
    assert response.status_code == 200
    assert isinstance(response.data, list)


@pytest.mark.django_db
def test_client_statistics(api_client):
    # Create test data (adjust as needed)
    client = Client.objects.create(full_name='test_client', birth_date=datetime.date.today())
    url = reverse('client-statistics', kwargs={'id': client.id})

    # Make a request to the view
    response = api_client.get(url)

    # Assert the response status code and content
    assert response.status_code == 200
    assert 'client_id' in response.data
    assert 'full_name' in response.data
    assert 'number_of_products_bought' in response.data
    assert 'amount_of_products' in response.data
