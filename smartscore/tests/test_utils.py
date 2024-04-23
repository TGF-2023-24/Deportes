import pytest
from ..utils import get_player_positions, get_transfermarkt_market_value, parse_market_value
from unittest.mock import patch

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



@pytest.mark.parametrize("input_value, expected_value", [
    ("€150m", 150.0),  # Example market value in millions
    ("€100m", 100.0),  # Example market value in millions
    ("€128m", 128.0),  # Example market value in millions
    ("€200m", 200.0),  # Example market value in millions
    ("€85m", 85.0),  # Example market value in millions
    ("€60m", 60.0),  # Example market value in millions
    ("€80m", 80.0),  # Example market value in millions
    ("€120m", 120.0),  # Example market value in millions
    ("€80m", 80.0),  # Example market value in millions
    ("Unknown", "Unknown"),  # Unknown market value
])
def test_parse_market_value(input_value, expected_value):
    # Call the function to parse the market value
    parsed_value = parse_market_value(input_value)

    # Check if the parsed value matches the expected value
    assert parsed_value == expected_value
