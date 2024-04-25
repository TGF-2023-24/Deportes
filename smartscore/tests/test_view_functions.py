import pytest
from django.http import JsonResponse
from ..views import position_stats_api, get_id_from_playerName, get_replacement_players, compare_players, replace_player
from ..models import Player, Position, Squad
from django.test import RequestFactory
import json
from django.core.exceptions import ObjectDoesNotExist

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
def sample_player():
    # Create a sample player for testing
    return    Player.objects.create(
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
def player1():
    return Player.objects.create(
        Name="Lionel Messi",
        Club="Paris Saint-Germain",
        League="Ligue 1",
        Nationality="Argentina",
        Pref_foot="Left",
        Age=34,
        Height=170,
        Weight=72,
        custom_id=3,
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
def sample_player1():
    # Create a sample player for testing
    return    Player.objects.create(
        custom_id=4,
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
def elbicho():
    return Player.objects.create(
        custom_id=5,  # Change the ID if needed
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
        Dist_90=8.0,  # Adjusted distance covered per 90 minutes
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

@pytest.mark.django_db
def test_position_stats_api(player):
    # Assuming you have the necessary setup to simulate a request
    request = None  # Simulate a request object, if needed
    position = Position.objects.create(name='DC')
    custom_id = player.custom_id  # Provide a custom_id for testing
    
    # Call the function and get the response
    response = position_stats_api(request, position.name, custom_id)

    # Check if the response is a JsonResponse
    assert isinstance(response, JsonResponse)

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_id_from_playerName_exists(rf, player):

    # Create a request with playerName and position parameters

    pos = Position.objects.create(name='ST')

    player.Pos.add(pos)

    request = rf.get('/get_id/', {'playerName': player.Name, 'position': pos.name})
    
    # Call the get_id_from_playerName function
    response = get_id_from_playerName(request,  player.Name, pos.name)
    
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

    # Deserialize the JSON content of the response
    data = json.loads(response.content)
    
    # Check if the response contains the expected custom_id
    assert data['id'] == player.custom_id

@pytest.mark.django_db
def test_get_id_from_playerName_not_exists(rf):
    pos = Position.objects.create(name='ST')

    # Create a request with playerName and position parameters for a non-existent player
    request = rf.get('/get_id/', {'playerName': 'Nonexistent Player', 'position':  pos.name})
    
    # Call the get_id_from_playerName function
    with pytest.raises(Player.DoesNotExist):
        get_id_from_playerName(request, 'Nonexistent Player',  pos.name)



@pytest.mark.django_db
def test_get_replacement_players(rf, player, sample_player, elbicho):
    # Create a squad and players
    # Replace the placeholders with appropriate objects for your model
    squad = Squad.objects.create(name='Test Squad')

    squad.players.add(player)
    pos = Position.objects.create(name='MC')
    player.Pos.add(pos)
    sample_player.Pos.add(pos)
    elbicho.Pos.add(pos)
    
    # Create a request with necessary parameters
    request = rf.get('/get-replacement-players/', {'position': 'MC', 'player': player.Name, 'squad_id': squad.id})
    
    # Call the get_replacement_players function
    response = get_replacement_players(request, 'MC', player.Name, squad.id)
    
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200


@pytest.mark.django_db
def test_compare_players(rf, player, sample_player):
    # Create a request with necessary parameters
    pos = Position.objects.create(name='MC')
    player.Pos.add(pos)
    sample_player.Pos.add(pos)

    request = rf.get('/compare-players/', {'player1': player.Name, 'player2': sample_player.Name, 'position': 'MC'})
    
    # Call the compare_players function
    response = compare_players(request, player.Name, sample_player.Name, 'MC')
    
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

@pytest.mark.django_db
def test_compare_players_multiple(rf, player1, sample_player1, player, sample_player):
    # Create a request with necessary parameters
    pos = Position.objects.create(name='MC')
    player1.Pos.add(pos)
    sample_player1.Pos.add(pos)
    player.Pos.add(pos)
    sample_player.Pos.add(pos)

    request = rf.get('/compare-players/', {'player1': player1.Name, 'player2': sample_player1.Name, 'position': 'MC'})
    
    # Call the compare_players function
    response = compare_players(request, player1.Name, sample_player1.Name, 'MC')

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200
    
    assert  '{"error": "Multiple players found or player does not exist"}' in response.content.decode("utf-8")


@pytest.mark.django_db
def test_replace_player(rf, player, sample_player):
    # Create a squad and players
    # Replace the placeholders with appropriate objects for your model
    squad = Squad.objects.create(name='Test Squad')
    squad.players.add(player)
    #squad.players.add(sample_player)
    old_player = player
    new_player = sample_player

    pos = Position.objects.create(name='MC')
    old_player.Pos.add(pos)
    new_player.Pos.add(pos)
    
    # Create a request with necessary parameters
    request = rf.post('/replace-player/', {'squad_id': squad.id, 'old_player': old_player.Name, 'new_player': new_player.Name, 'pos': 'MC'})
    
    # Call the replace_player function
    response = replace_player(request, squad.id, old_player.Name, new_player.Name, 'MC')

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

    # Check if the old player is removed from the squad
    assert old_player not in squad.players.all()

    # Check if the new player is added to the squad
    assert new_player in squad.players.all()

@pytest.mark.django_db
def test_replace_player_exception(rf):
    # Create a request with invalid parameters
    request = rf.post('/replace-player/', {'squad_id': 9999, 'old_player': 'Nonexistent Player', 'new_player': 'Another Player', 'pos': 'MC'})
    
    # Call the replace_player function
    response = replace_player(request, 9999, 'Nonexistent Player', 'Another Player', 'MC')

    # Check if the response status code is 500 (Internal Server Error)
    assert response.status_code == 500

    # Check if the response contains the expected error message
    assert response.content.decode("utf-8") == '{"error": "Squad matching query does not exist."}'

