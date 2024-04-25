import json
from django.contrib.auth.models import User
from django.test import RequestFactory
from django.urls import reverse
import pytest
from ..views import squad_stats_api, player_smartscore_api
from ..models import Player, UserProfile, Position
from django.contrib.auth.models import AnonymousUser

@pytest.fixture
def rf():
    return RequestFactory()

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
        Asis=4,
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
        Dist_90=12,
        Key_tck_90=1.2,
        Key_hdr_90=0.8,
        Blocks_90=2.5,
        Clr_90=3.0,
        Int_90=1.9,
        Hdr_rat=85,
        Tackles_rat=75,
        Gl_mistake=1,
        Pass_rat=77,
        Pr_pass_90=85,
        Key_pass_90=2.0,
        Cr_c_90=3.5,
        Cr_c_acc=80,
        Ch_c_90=2.1,
        Drb_90=1.5,
        Poss_lost_90=8.5,
        Shot_rat=80,
        Conv_rat=15,
        Dorsal=10,
        Country_league="Test Country",
        market_value="10"
    )

@pytest.fixture
def player2():
    return Player.objects.create(
        custom_id=2,
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
        Asis_90=0.20,
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

@pytest.fixture
def elbicho():
    return Player.objects.create(
        custom_id=3,  # Change the ID if needed
        Name="El Bicho",  # Change the name if needed
        Club="Test Club",
        Nationality="Test Nationality",
        International_match=0,
        League="Test League",
        Pref_foot="Left",
        Age=25,
        Height=180,
        Weight=75,
        Salary=60000,  # Adjusted salary
        CAbil=85,  # Adjusted ability
        Pot_abil=95,  # Adjusted potential ability
        Strater_match=25,  # Adjusted starting matches
        Res_match=15,  # Adjusted reserve matches
        Min=2000,  # Adjusted minutes played
        Goal=8,  # Adjusted goals scored
        Asis=5,  # Adjusted assists
        xG=6.5,  # Adjusted expected goals
        Gol_90=0.35,  # Adjusted goals per 90 minutes
        Asis_90=0.25,  # Adjusted assists per 90 minutes
        Goal_allowed=12,  # Adjusted goals allowed
        Clean_sheet=4,  # Adjusted clean sheets
        Sv_rat=85,  # Adjusted save rate
        xSv_rat=80,  # Adjusted expected save rate
        Pen_saved_rat=75,  # Adjusted penalty save rate
        Faga=25,  # Adjusted aerial duels won
        Fcomm=20,  # Adjusted aerial duels lost
        Yel=3,  # Adjusted yellow cards
        Red=1,  # Adjusted red cards
        Dist_90=10.0,  # Adjusted distance covered per 90 minutes
        Key_tck_90=1.5,  # Adjusted key tackles per 90 minutes
        Key_hdr_90=1.0,  # Adjusted key headers per 90 minutes
        Blocks_90=3.0,  # Adjusted blocks per 90 minutes
        Clr_90=3.5,  # Adjusted clearances per 90 minutes
        Int_90=2.0,  # Adjusted interceptions per 90 minutes
        Hdr_rat=90,  # Adjusted header success rate
        Tackles_rat=80,  # Adjusted tackle success rate
        Gl_mistake=2,  # Adjusted goalkeeping mistakes
        Pass_rat=95,  # Adjusted passing success rate
        Pr_pass_90=90,  # Adjusted progressive passes per 90 minutes
        Key_pass_90=2.5,  # Adjusted key passes per 90 minutes
        Cr_c_90=4.0,  # Adjusted crosses per 90 minutes
        Cr_c_acc=85,  # Adjusted cross accuracy
        Ch_c_90=2.5,  # Adjusted chances created per 90 minutes
        Drb_90=2.0,  # Adjusted dribbles per 90 minutes
        Poss_lost_90=7.5,  # Adjusted possessions lost per 90 minutes
        Shot_rat=85,  # Adjusted shooting accuracy
        Conv_rat=20,  # Adjusted conversion rate
        Dorsal=11,  # Adjusted squad number
        Country_league="Test Country",
        market_value="12M"  # Adjusted market value
    )


@pytest.fixture 
def position():
    return Position.objects.create(name='MC')

@pytest.mark.django_db
def test_squad_stats_api_pos(authenticated_request, player, position, player2, elbicho):
    # Create a list of player names
    players_list = [player.Name]
    player.Pos.add(position)
    player2.Pos.add(position)
    elbicho.Pos.add(position)

    # Serialize the list of players to JSON
    players_json = json.dumps(players_list)

    # Make a request to the squad_stats_api endpoint
    response = squad_stats_api(authenticated_request, 'MC', players_json)

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200


@pytest.mark.django_db
def test_player_smartscore_api_authenticated(authenticated_request, player, position):
    # Make a request to the player_smartscore_api endpoint
    player.Pos.add(position)
    response = player_smartscore_api(authenticated_request, 'MC', player.custom_id)

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200


@pytest.mark.django_db
def test_player_smartscore_api_unauthenticated(rf, player, position):
    # Create an unauthenticated request
    request = rf.get('/fake-path/')
    request.user = AnonymousUser()  # Set the user to be anonymous

    # Make a request to the player_smartscore_api endpoint
    player.Pos.add(position)
    response = player_smartscore_api(request, 'MC', player.custom_id)

    assert response.status_code == 200
