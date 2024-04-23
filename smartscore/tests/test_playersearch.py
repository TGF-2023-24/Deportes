import pytest
from django.test import Client
from django.contrib.auth.models import User
from ..models import Player, Position
from ..views import advanced_search
from django.http import JsonResponse
from django.test import RequestFactory
from json.decoder import JSONDecodeError


@pytest.fixture
def client():
    return Client()

@pytest.mark.django_db
def test_search_player(client):
    # Create some players for testing
    messi = Player.objects.create(
        Name="Lionel Messi",
        Club="Paris Saint-Germain",
        League="Ligue 1",
        Nationality="Argentina",
        Pref_foot="Left",
        Age=34,
        Height=170,
        Weight=72,
        custom_id=1,
        Salary=50000,
        CAbil=80,
        Pot_abil=90,
        Strater_match=20,
        International_match=20,
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
        market_value="10M"
    )
    cr7 = Player.objects.create(
        Name="Cristiano Ronaldo",
        Club="Manchester United",
        League="Premier League",
        Nationality="Portugal",
        Pref_foot="Right",
        Age=37,
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

    # Create positions
    dc = Position.objects.create(name="DC")
    dm = Position.objects.create(name="DM")

    # Assign positions to players
    messi.Pos.add(dc)
    cr7.Pos.add(dm)
    
    # Test searching for Messi
    response = client.post('/search_player/', {'q': 'Messi'})
    assert response.status_code == 200
    assert 'Lionel Messi' in response.content.decode()

    # Test searching for Ronaldo
    response = client.post('/search_player/', {'q': 'Ronaldo'})
    assert response.status_code == 200
    assert 'Cristiano Ronaldo' in response.content.decode()

    # Test searching for a non-existent player
    response = client.post('/search_player/', {'q': 'Neymar'})
    assert response.status_code == 200
    assert 'No players found' in response.content.decode('utf-8')

@pytest.mark.django_db
def test_advanced_search(client):
    # Test sending a GET request to advanced_search without parameters
    response = client.get('/advanced_search/')
    assert response.status_code == 200

    # Test sending a valid advanced search request
    response = client.get('/advanced_search/', {'selectedPositions': ['Forward'], 'filters': '[{"property": "Age", "type": "greater", "value": 35}]'})
    assert response.status_code == 302

    # Test sending an invalid advanced search request
    response = client.get('/advanced_search/', {'filters': '[{"property": "Age", "type": "greater", "value": 50}]'})
    assert response.status_code == 200

#test search player when method is not post
def test_search_player_get(client):
    response = client.get('/search_player/')
    assert response.status_code == 200
    assert 'No players found' in response.content.decode('utf-8')


@pytest.mark.django_db
def test_advanced_search_exceptions():
    factory = RequestFactory()

    # Test sending a request with invalid JSON format
    request_invalid_json = factory.get('/advanced_search/', {'selectedPositions': ['Forward'], 'filters': 'invalid-json'})
    with pytest.raises(JSONDecodeError):
        response_invalid_json = advanced_search(request_invalid_json)

    # Test sending a request that triggers other exceptions
    request_other_exception = factory.get('/advanced_search/')
    response_other_exception = advanced_search(request_other_exception)
