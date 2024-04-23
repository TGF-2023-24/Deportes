import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.contrib import messages
from django.contrib.auth import authenticate
from ..models import UserProfile

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def create_user_with_profile():
    user = User.objects.create_user(username="testuser", password="testpassword", email="test@example.com")
    profile = UserProfile.objects.create(user=user)
    return user

@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create_user(
        username="testuser",
        password="testpassword",
        email="prueba@gmail.com"
    )
    assert User.objects.count() == 1
    assert user.username == "testuser"


@pytest.mark.django_db
def test_user_login(client, create_user_with_profile):
    user = create_user_with_profile
    login_data = {
        'username': 'testuser',
        'password': 'testpassword',
        'next': '/my_squads/'  # Specify the URL to redirect to after successful login

    }
    response = client.post('/login/', login_data, follow=True)
    
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

    # Check if the user is authenticated in the context
    assert response.context['user'].is_authenticated

    # Check if the redirect URL matches the next_url parameter
    assert response.redirect_chain == [('/my_squads/', 302)]

@pytest.mark.django_db
def test_login_user_failed_authentication(client):
    # Create a user
    User.objects.create_user(username="testuser", password="testpassword")

    # Simulate a POST request with invalid login credentials
    response = client.post('/login/', {'username': 'testuser', 'password': 'wrongpassword'}, follow=True)

    # Check if the response status code is 200
    assert response.status_code == 200

@pytest.mark.django_db
def test_user_already_authenticated(client):
    # Create a user
    User.objects.create_user(username="testuser", password="testpassword")

    # Authenticate the user
    client.login(username="testuser", password="testpassword")

    # Simulate a GET request to the login page
    response = client.get('/login/')

    # Check if the response status code is 302 (redirect)
    assert response.status_code == 302

    # Check if the user is authenticated
    assert response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
def test_user_logout(client):
    User.objects.create_user(
        username="testuser",
        password="testpassword",
        email="prueba@gmail.com"
    )
    login_data = {
        'username': 'testuser',
        'password': 'testpassword'
    }
    client.post('/login/', login_data, follow=True)
    response = client.get('/logout/', follow=True)
    assert response.status_code == 200
    assert not response.context['user'].is_authenticated


@pytest.mark.django_db
def test_signup_user(client):
    # Test when user is already authenticated
    client.force_login(User.objects.create_user(username='existing_user', password='password123'))
    response = client.get('/signup/')
    assert response.status_code == 302  # Redirect to home page  

    # Test when form is submitted with valid data
    client.logout()  # Logout to test signup process
    response = client.post('/signup/', {'username': 'new_user', 'email': 'new_user@example.com', 'password1': 'newpassword123', 'password2': 'newpassword123'})
    assert response.status_code == 302  # Redirect to home page  
    assert User.objects.count() == 2


    ##test when form is submitted with invalid data
    client.logout()
    response = client.post('/signup/', {'username': '', 'email': '  ', 'password1': 'newpassword123', 'password2': 'newpassword123'})
    assert response.status_code == 200
    assert User.objects.count() == 2