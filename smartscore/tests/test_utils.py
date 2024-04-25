import pytest
from ..utils import get_player_positions, get_transfermarkt_market_value, parse_market_value, get_dot_positions, get_max_min_attribute
from unittest.mock import patch
from ..models import Position, Player
from django.core.exceptions import ObjectDoesNotExist

def test_get_player_positions():
    # Test with a single position without specification
    assert get_player_positions("DC") == ["DC"]

    # Test with multiple positions separated by '/'
    assert get_player_positions("DC/MC") == ["DC", "MC"]

    # Test with a single position with specification
    assert get_player_positions("AM(R)") == ["AMR"]

    # Test with multiple positions with specification
    assert get_player_positions("AM(R),AM(C)") == ["AMR", "AMC"]

    # Test with a combination of positions and specifications
    assert get_player_positions("AM(RC),AM(L)") == ['AMR', 'AMC', 'AML']

    # Test with a goalkeeper position (no specification)
    assert get_player_positions("GK") == ["GK"]

    # Test with a combination of positions and specifications
    assert get_player_positions("AM(R),DC,GK") == ["AMR", "DC", "GK"]

    # Test with positions and no specification
    assert get_player_positions("MC,DC,GK") == ["MC", "DC", "GK"]

    # Test with an empty string
    assert get_player_positions("") == ['']

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
        Clr_90=4.0,
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


@pytest.mark.django_db
def test_dot_position(player):
    pos1 = Position.objects.create(name="GK")
    pos2 = Position.objects.create(name="ML")
    pos3 = Position.objects.create(name="MC")
    pos4 = Position.objects.create(name="MR")

    player.Pos.add(pos1, pos2, pos3, pos4)

    assert get_dot_positions(player.Pos) == [{'left': 250, 'top': 750}, {'left': 75, 'top': 400}, {'left': 250, 'top': 400}, {'left': 425, 'top': 400}]

@pytest.mark.parametrize("input_name, expected_value", [
    ("Lionel Messi", 150.0),  # Example market value in millions
    ("Cristiano Ronaldo", 100.0),  # Example market value in millions
    ("Neymar", 128.0),  # Example market value in millions
    ("Kylian Mbappe", 200.0),  # Example market value in millions
    ("Marcus Rashford", 85.0),  # Example market value in millions
    ("Frenkie de Jong", 60.0),  # Example market value in millions
    ("Joao Felix", 80.0),  # Example market value in millions
    ("Mohamed Salah", 120.0),  # Example market value in millions
    ("Paul Pogba", 80.0),  # Example market value in millions
])
def test_get_transfermarkt_market_value(input_name, expected_value):
    # Mock the requests.get method to simulate responses
    with patch('requests.get') as mocked_get:
        # Set up the mocked response
        mocked_get.return_value.status_code = 200
        mocked_get.return_value.json.return_value = {
            "results": [
                {"marketValue": f"€{expected_value}m"}
            ]
        }

        # Call the function to get the market value
        market_value = get_transfermarkt_market_value(input_name)

        # Check if the market value matches the expected value or is 'Unknown'
        assert market_value == expected_value or market_value == 'Unknown'

@pytest.mark.parametrize("input_name, expected_value", [
    ("Lionel Messi", 150.0),  # Example market value in millions
])

def test_get_transfermarkt_market_value_not_200(input_name, expected_value):
    # Mock the requests.get method to simulate responses
    with patch('requests.get') as mocked_get:
        # Set up the mocked response
        mocked_get.return_value.status_code = 404
        mocked_get.return_value.json.return_value = {
            "results": [
                {"marketValue": f"€{expected_value}m"}
            ]
        }

        # Call the function to get the market value
        market_value = get_transfermarkt_market_value(input_name)

        # Check if the market value matches the expected value or is 'Unknown'
        assert market_value == expected_value or market_value == 'Unknown'


@pytest.mark.parametrize("input_value, expected_value", [
    ("€150m", 150.0),  # Example market value in millions
    ("€100m", 100.0),  # Example market value in millions
    ("€128m", 128.0),  # Example market value in millions
    ("€200m", 200.0),  # Example market value in millions
    ("€85m", 85.0),  # Example market value in millions
    ("€60m", 60.0),  # Example market value in millions
    ("€80m", 80.0),  # Example market value in millions
    ("€120k",0.12),  # Example market value in millions
    ("€80s", "Unknown"),  # Example market value in millions
    ("Unknown", "Unknown"),  # Unknown market value
])
def test_parse_market_value(input_value, expected_value):
    # Call the function to parse the market value
    parsed_value = parse_market_value(input_value)

    # Check if the parsed value matches the expected value
    assert parsed_value == expected_value


@pytest.mark.django_db
def test_get_max_min_attribute( player, player2):

    position = Position.objects.create(name="MC")
    player.Pos.add(position)
    player2.Pos.add(position)

    # Call the function
    max_value, min_value = get_max_min_attribute("Clr_90", "MC")

    # Check the results
    assert max_value == 4.0
    assert min_value == 3.0

@pytest.mark.django_db
def test_get_max_min_attribute_invalid_position():
    # Test case for an invalid position
    with pytest.raises(ObjectDoesNotExist):
        get_max_min_attribute('test_attribute', 'Invalid Position')

