import pytest
from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from django.test import Client
from django.contrib.messages import get_messages
from ..views import about, search_results, settings
from ..models import Player, Position

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def cr7():
    return Player.objects.create(
        Name="Cristiano Ronaldo",
        Club="Manchester United",
        League="Premier League",
        Nationality="Portugal",
        Pref_foot="Right",
        Age=25,
        Height=187,
        Weight=83,
        custom_id=2,
        Salary=60000,
        International_match=10,
        CAbil=85,
        Pot_abil=95,
        Strater_match=25,
        Res_match=15,
        Min=1800,
        Goal=7,
        Asis=5,
        xG=6.5,
        Gol_90=0.35,
        Asis_90=0.25,
        Goal_allowed=15,
        Clean_sheet=5,  
        Sv_rat=85,
        xSv_rat=80,
        Pen_saved_rat=75,
        Faga=25,
        Fcomm=20,
        Yel=3,
        Red=0,
        Dist_90=10.5,
        Key_tck_90=1.5,
        Key_hdr_90=1.0,
        Blocks_90=3.5,
        Clr_90=4.0,
        Int_90=2.0,
        Hdr_rat=90,
        Tackles_rat=80,
        Gl_mistake=2,
        Pass_rat=95,
        Pr_pass_90=90,
        Key_pass_90=2.5,
        Cr_c_90=4.0,
        Cr_c_acc=85,
        Ch_c_90=2.5,
        Drb_90=2.0,
        Poss_lost_90=9.5,
        Shot_rat=85,
        Conv_rat=20,
        Dorsal=7,
        Country_league="Test Country",
        market_value="15M"
    )

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
def test_search_results_with_noresults(client):
    response = client.get(reverse('search_results'), {'positions': 'Forward,Midfielder', 'filters': '[{"attribute": "age", "min": 20}]'})
    assert response.status_code == 200
    

@pytest.mark.django_db
def test_search_results_invalid_json(client):
    response = client.get(reverse('search_results'), {'positions': 'Forward', 'filters': 'invalid-json'})
    assert response.status_code == 200

@pytest.mark.django_db
def test_search_results_valid(client, cr7):
    pos = Position.objects.create(name="STC")
    cr7.Pos.add(pos)
    response = client.get(reverse('search_results'), {'positions': 'STC',  'filters': '[{"property": "Age", "type": "less", "value": 35}]'})
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

@pytest.mark.django_db
def test_settings_post_authenticated_valid_user(authenticated_client):
    data = {
        'username': 'newusername',
        'email': 'newemail@example.com',
    }
    response = authenticated_client.post(reverse('settings'), data)
    assert response.status_code == 200
    messages = list(get_messages(response.wsgi_request))
    print(messages)
    assert len(messages) == 1  

      

@pytest.mark.django_db
def test_settings_post_authenticated_valid_pwd(authenticated_client):
    data = {
        'old_password': 'testpassword',
        'new_password1': 'NewTesting@12',
        'new_password2': 'NewTesting@12'
    }
    response = authenticated_client.post(reverse('settings'), data)
    assert response.status_code == 302
    messages = list(get_messages(response.wsgi_request))
    print(messages)
    assert len(messages) == 1  

@pytest.mark.django_db
def test_settings_post_authenticated_invalid_password(authenticated_client):
    data = {
        'username': 'newusername',
        'email': 'newemail@example.com',
        'old_password': 'wrongpassword',  # Invalid old password
        'new_password1': 'newpassword',
        'new_password2': 'newpassword'
    }
    response = authenticated_client.post(reverse('settings'), data)
    assert response.status_code == 200
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1  # Expect only one success message for user update, password update should fail


