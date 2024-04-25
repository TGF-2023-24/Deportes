# test_future_scope.py
import json
import pytest
from django.contrib.auth.models import User
from django.test import RequestFactory
from ..models import League, UserProfile
from ..views import futureScope, save_futureScope, edit_futureScope
from django.http import JsonResponse


@pytest.fixture
def user():
    # Create a user for testing
    user = User.objects.create_user(username='test_user', password='test_password')
    UserProfile.objects.create(
        user=user, 
        budget=100,
        expectations=1,
        league = "test league",)  # Create a related UserProfile
    return user

@pytest.fixture
def sample_league1():
    # Create a sample league for testing
    league = League.objects.create(name='Test League', country_league='Test Country')
    return league



@pytest.mark.django_db
def test_futureScope_view(user):
    # Test futureScope view function

    request = RequestFactory().get('/future-scope/')
    request.user = user
    response = futureScope(request)
    assert response.status_code == 200
    # Add more assertions as needed



@pytest.mark.django_db
def test_save_futureScope_view(user, sample_league1):
    # Test save_futureScope view function
    request = RequestFactory().post('/save-future-scope/', json.dumps({
        'transfer_budget': 150000,
        'selected_league': sample_league1.name,
        'selected_expectations': 2
    }), content_type='application/json')
    request.user = user
    response = save_futureScope(request)
    assert response.status_code == 200
    # Add more assertions as needed


@pytest.mark.django_db
def test_save_futureScope_invalid_request_method(user, sample_league1):
    # Test save_futureScope view function with an invalid request method
    request = RequestFactory().get('/save-future-scope/')
    request.user = user
    
    # Call the save_futureScope view function
    response = save_futureScope(request)
    
    # Check if the response status code is 400 (Bad Request)
    assert response.status_code == 400
    
    # Check if the response contains the expected error message
    expected_error_message = {'error': 'Invalid request method'}
    assert response.content == JsonResponse(expected_error_message, status=400).content

@pytest.mark.django_db
def test_edit_futureScope_view(user, sample_league1):
    # Test edit_futureScope view function
    request = RequestFactory().get('/edit-future-scope/')
    request.user = user
    response = edit_futureScope(request)
    assert response.status_code == 200
    # Add more assertions as needed
