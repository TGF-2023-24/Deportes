import json
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from ..models import Player, UserProfile, Shortlist, Position

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
def shortlist(user, sample_player1, sample_player2):
    # Create a shortlist for testing
    shortlist = Shortlist.objects.create(name='Recommendations for Agile DC players with Left foot')
    shortlist.players.add(sample_player1, sample_player2)
    Usermodel = UserProfile.objects.get(user=user)
    Usermodel.shortlist.add(shortlist)

    return shortlist

@pytest.fixture
def sample_player1():
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

@pytest.fixture
def sample_player2():
    # Create a sample player for testing
    return    Player.objects.create(
        custom_id=2,
        Name="Test Player2",
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
        Gol_90=0.3,
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
def test_get_recommendations_auth_noplayers(authenticated_client, user, sample_player1, sample_player2):
    pos = Position.objects.create(name='STC')   
    sample_player1.Pos.add(pos)
    sample_player2.Pos.add(pos)

    # Simulate a GET request to get recommendations
    url = reverse('get_recommendations')
    response = authenticated_client.get(url, data={'positions': 'STC', 'attributes': 'Hdr_rat,Conv_rat,Gol_90', 'foot': 'Right'})
    
    # Check that the response is successful
    assert response.status_code == 200
    
    # Check that the response contains JSON data
    assert response['content-type'] == 'application/json'
    
    # Check the response data
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0  # Check the number of recommendations

@pytest.mark.django_db
def test_get_recommendations_auth_success(authenticated_client, user, sample_player1, sample_player2):
    pos = Position.objects.create(name='STC')   
    sample_player1.Pos.add(pos)
    sample_player2.Pos.add(pos)

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
    assert len(data) == 1  # Check the number of recommendations

@pytest.mark.django_db
def test_get_recommendations_unauth( user, sample_player1):
    # Create a test client
    client = Client()

    # Simulate a GET request to get recommendations
    url = reverse('get_recommendations')
    response = client.get(url, data={'positions': 'STC', 'attributes': 'Hdr_rat,Conv_rat,Gol_90', 'foot': 'Left'})
    
    # Check that the response is successful
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_recommendations_unauth_noattr( user, sample_player1):
    # Create a test client
    client = Client()

    # Simulate a GET request to get recommendations
    url = reverse('get_recommendations')
    response = client.get(url, data={'positions': 'STC', 'attributes': '', 'foot': 'Left'})
    
    # Check that the response is successful
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_recommendations_unauth_feet( user, sample_player1):
    # Create a test client
    client = Client()

    # Simulate a GET request to get recommendations
    url = reverse('get_recommendations')
    response = client.get(url, data={'positions': 'STC', 'attributes': 'Hdr_rat,Conv_rat,Gol_90', 'foot': 'Left, Right'})
    
    # Check that the response is successful
    assert response.status_code == 200

@pytest.mark.django_db
def test_get_recommendations_unauth_nofeet( user, sample_player1):
    # Create a test client
    client = Client()

    # Simulate a GET request to get recommendations
    url = reverse('get_recommendations')
    response = client.get(url, data={'positions': 'STC', 'attributes': 'Hdr_rat,Conv_rat,Gol_90', 'foot': ''})
    
    # Check that the response is successful
    assert response.status_code == 200

@pytest.mark.django_db
def test_save_recommendations_new_shortlist(authenticated_client, user, sample_player1):
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


#exsting and player in shortlist
@pytest.mark.django_db
def test_save_recommendations_existing_shortlist(authenticated_client, user, shortlist, sample_player1):
    # Simulate a POST request to save recommendations
    url = reverse('save_recommendations')
    data = {
        'position': 'DC',
        'archetype': 'Agile',
        'foot': 'Left',
        'recommendation': {'name': sample_player1.Name}
    }
    response = authenticated_client.post(url, data=json.dumps(data), content_type='application/json')
    
    # Check that the response is successful
    assert response.status_code == 200
    
    # Check that the response contains JSON data
    assert response['content-type'] == 'application/json'
    
    # Check the response message
    data = response.json()
    assert 'message' in data
    assert data['message'] == 'Player Test Player is already in the shortlist.'


#player not in database
@pytest.mark.django_db
def test_save_recommendations_no_player(client):
    # Simulate a GET request to save recommendations
    url = reverse('save_recommendations')
    data = {
        'position': 'DC',
        'archetype': 'Agile',
        'foot': 'Left',
        'recommendation': {'name': 'not in database'}
    }
    response = client.post(url, data=json.dumps(data), content_type='application/json')   

    assert response.status_code == 302

@pytest.mark.django_db
def test_not_post_request(authenticated_client, user, sample_player1):
    # Simulate a GET request to save recommendations
    url = reverse('save_recommendations')
    response = authenticated_client.get(url)   

    # Check if the response status code is 400
    assert response.status_code == 400

    # Check if the response contains the expected JSON error message
    expected_error_message = "Invalid method. This endpoint only accepts POST requests."
    assert response.json() == {'error': expected_error_message}