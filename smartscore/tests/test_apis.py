import json
from django.contrib.auth.models import User
from django.test import RequestFactory
from django.urls import reverse
import pytest
from ..views import squad_stats_api, player_smartscore_api
from ..models import Player, UserProfile, Position


@pytest.fixture
def authenticated_user():
    user = User.objects.create_user(username='testuser', password='testpassword')
    UserProfile.objects.create(user=user)
    return user


@pytest.fixture
def authenticated_request(rf, authenticated_user):
    request = rf.get('/fake-path/')
    request.user = authenticated_user
    return request


@pytest.fixture
def player():
    return Player.objects.create(
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
        market_value="10"
    )

@pytest.fixture 
def position():
    return Position.objects.create(name='MC')

@pytest.mark.django_db
def test_squad_stats_api(authenticated_request, player, position):
    # Create a list of player names
    players_list = [player.Name]
    player.Pos.add(position)

    # Serialize the list of players to JSON
    players_json = json.dumps(players_list)

    # Make a request to the squad_stats_api endpoint
    response = squad_stats_api(authenticated_request, 'MC', players_json)

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200


@pytest.mark.django_db
def test_player_smartscore_api(authenticated_request, player, position):
    # Make a request to the player_smartscore_api endpoint
    player.Pos.add(position)
    response = player_smartscore_api(authenticated_request, 'MC', player.custom_id)

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200
