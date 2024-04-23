import pytest
from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from django.test import Client
from django.contrib.messages import get_messages
from ..views import about, search_results, settings

@pytest.fixture
def client():
    return Client()

def test_about_view():
    request = RequestFactory().get('/about/')
    response = about(request)
    assert response.status_code == 200

def test_recommended_signings_view(client):
    response = client.get(reverse('recommended_signings'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_search_results_no_results(client):
    response = client.get(reverse('search_results'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_search_results_with_results(client):
    response = client.get(reverse('search_results'), {'positions': 'Forward,Midfielder', 'filters': '[{"attribute": "age", "min": 20}]'})
    assert response.status_code == 200

@pytest.mark.django_db
def test_search_results_invalid_json(client):
    response = client.get(reverse('search_results'), {'positions': 'Forward', 'filters': 'invalid-json'})
    assert response.status_code == 200

@pytest.fixture
def authenticated_user():
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user

@pytest.fixture
def authenticated_client(authenticated_user):
    client = Client()
    client.login(username='testuser', password='testpassword')
    return client

@pytest.mark.django_db
def test_settings_get_authenticated(authenticated_client):
    response = authenticated_client.get(reverse('settings'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_settings_get_anonymous(client):
    response = client.get(reverse('settings'))
    assert response.status_code == 302
    assert response.url == '/login/?next=/settings/'

@pytest.mark.django_db
def test_settings_post_authenticated(authenticated_client):
    data = {
        'username': 'newusername',
        'email': 'newemail@example.com',
        'old_password': 'testpassword',
        'new_password1': 'newpassword',
        'new_password2': 'newpassword'
    }
    response = authenticated_client.post(reverse('settings'), data)
    assert response.status_code == 200
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1

@pytest.mark.django_db
def test_settings_post_invalid_form(authenticated_client):
    response = authenticated_client.post(reverse('settings'), {})
    assert response.status_code == 200
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 0
