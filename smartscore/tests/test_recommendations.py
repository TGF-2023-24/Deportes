import json
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from ..models import Player, UserProfile, Shortlist

@pytest.fixture
def client():
    # Create a test client
    return Client()

@pytest.fixture
def user():
    # Create a user for testing
    user = User.objects.create_user(username='test_user', password='test_password')
    UserProfile.objects.create(user=user)  # Create a related UserProfile
    return user

@pytest.fixture
def authenticated_client(client, user):
    # Authenticate the client with the test user
    client.login(username='test_user', password='test_password')
    return client

@pytest.fixture
def sample_player():
    # Create a sample player for testing
    return    Player.objects.create(
        custom_id=1,
        Name="Test Player",
        Club="Test Club",
        Nationality="Test Nationality",
        International_match=0,
        League="Test League",
        Pref_foot="Left",
        Age=25,
        Height=180,
        Weight=75,
        Salary=50000,
        CAbil=80,
        Pot_abil=90,
        Strater_match=20,
        Res_match=10,
        Min=1800,
        Goal=5,
        Asis=3,
        xG=4.5,
        Gol_90=0.25,
        Asis_90=0.15,
        Goal_allowed=10,
        Clean_sheet=3,
        Sv_rat=80,
        xSv_rat=75,
        Pen_saved_rat=70,
        Faga=20,
        Fcomm=15,
        Yel=2,
        Red=0,
        Dist_90=9.5,
        Key_tck_90=1.2,
        Key_hdr_90=0.8,
        Blocks_90=2.5,
        Clr_90=3.0,
        Int_90=1.8,
        Hdr_rat=85,
        Tackles_rat=75,
        Gl_mistake=1,
        Pass_rat=90,
        Pr_pass_90=85,
        Key_pass_90=2.0,
        Cr_c_90=3.5,
        Cr_c_acc=80,
        Ch_c_90=2.2,
        Drb_90=1.5,
        Poss_lost_90=8.5,
        Shot_rat=80,
        Conv_rat=15,
        Dorsal=10,
        Country_league="Test Country",
        market_value="10"
    )

@pytest.mark.django_db
def test_get_recommendations(authenticated_client, user, sample_player):
    # Simulate a GET request to get recommendations
    url = reverse('get_recommendations')
    response = authenticated_client.get(url, data={'positions': 'STC', 'attributes': 'Hdr_rat,Conv_rat,Gol_90', 'foot': 'Left'})
    
    # Check that the response is successful
    assert response.status_code == 200
    
    # Check that the response contains JSON data
    assert response['content-type'] == 'application/json'
    
    # Check the response data
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0  # Assuming there are no recommendations for this user yet

@pytest.mark.django_db
def test_save_recommendations(authenticated_client, user, sample_player):
    # Simulate a POST request to save recommendations
    url = reverse('save_recommendations')
    data = {
        'position': 'DC',
        'archetype': 'Agile',
        'foot': 'Left',
        'recommendation': {'name': 'Test Player'}
    }
    response = authenticated_client.post(url, data=json.dumps(data), content_type='application/json')
    
    # Check that the response is successful
    assert response.status_code == 200
    
    # Check that the response contains JSON data
    assert response['content-type'] == 'application/json'
    
    # Check the response message
    data = response.json()
    assert 'message' in data
    assert data['message'] == 'Player Test Player saved successfully.'
