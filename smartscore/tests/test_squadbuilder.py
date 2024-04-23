import pytest
from django.contrib.auth.models import User
from django.test import RequestFactory
from django.urls import reverse
from ..views import squad_builder, squad_players, players_by_position
from django.test import Client
from ..models import Squad, UserProfile, Player, Position

@pytest.fixture
def rf():
    return RequestFactory()

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
        market_value="10M"
    )

@pytest.fixture
def squad():
    return Squad.objects.create(name='Test Squad')

@pytest.fixture
def user():
    user = User.objects.create_user(username='testuser', password='testpassword')
    user_profile = UserProfile.objects.create(user=user)
    return user

@pytest.mark.django_db
def test_squad_builder_view(rf, user):
    # Create a request with an authenticated user
    request = rf.get(reverse('squad_builder'))
    request.user = user
    
    # Call the squad_builder view function
    response = squad_builder(request)
    
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

@pytest.mark.django_db
def test_squad_players_view(rf):
    # Create a squad ID for testing
    squad_id = 1
    
    # Create a request with no parameters
    request = rf.get(reverse('squad_players', kwargs={'squad_id': squad_id}))
    
    # Call the squad_players view function
    response = squad_players(request, squad_id)
    
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

@pytest.mark.django_db
def test_players_by_position_view(rf, squad, player):
    # get squad id and create a position for testing, also add player to squad
    squad_id = squad.id
    position = Position.objects.create(name='ST')
    player.Pos.add(position)

    squad.players.add(player)

    #pass possition as a list
    position_list = ['ST', 'LW']

    # Create a request with no parameters
    request = rf.get(reverse('players_by_position', kwargs={'squad_id': squad_id, 'position': position_list}))
    
    # Call the players_by_position view function
    response = players_by_position(request, squad_id, position)
    
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200
