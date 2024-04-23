# test_future_scope.py

import json
import pytest
from django.contrib.auth.models import User
from django.test import RequestFactory
from ..models import League, UserProfile
from ..views import futureScope, save_futureScope, edit_futureScope

@pytest.fixture
def user():
    # Create a user for testing
    user = User.objects.create_user(username='test_user', password='test_password')
    UserProfile.objects.create(user=user)  # Create a related UserProfile
    return user

@pytest.fixture
def sample_league():
    # Create a sample league for testing
    league = League.objects.create(name='Test League', country_league='Test Country')
    return league

@pytest.fixture
def sample_user_profile(user, sample_league):
    # Create a sample user profile for testing
    user_profile, created = UserProfile.objects.get_or_create(user=user, defaults={'league': sample_league.name, 'budget': 100000, 'expectations':1})
    return user_profile

@pytest.mark.django_db
def test_futureScope_view(user, sample_league):
    # Test futureScope view function
    request = RequestFactory().get('/future-scope/')
    request.user = user
    response = futureScope(request)
    assert response.status_code == 200
    # Add more assertions as needed

@pytest.mark.django_db
def test_save_futureScope_view(user, sample_league):
    # Test save_futureScope view function
    request = RequestFactory().post('/save-future-scope/', json.dumps({
        'transfer_budget': 150000,
        'selected_league': sample_league.name,
        'selected_expectations': 2
    }), content_type='application/json')
    request.user = user
    response = save_futureScope(request)
    assert response.status_code == 200
    # Add more assertions as needed

@pytest.mark.django_db
def test_edit_futureScope_view(user, sample_league, sample_user_profile):
    # Test edit_futureScope view function
    request = RequestFactory().get('/edit-future-scope/')
    request.user = user
    response = edit_futureScope(request)
    assert response.status_code == 200
    # Add more assertions as needed
