from django.db.models import Avg, Max, Min, Q
from .models import Player, Position, Squad
from .dictionary import stats_position_dictionary
import requests

def get_dot_positions(player_pos):
    position_mapping = {
        'GK': {'default_top': 750},  # Goalkeeper
        'D': {'default_top': 650},   # Defender
        'WB': {'default_top': 525},  # Wing-back
        'DM': {'default_top': 525},  # Defensive midfielder
        'M': {'default_top': 400},   # Midfielder
        'AM': {'default_top': 250},  # Attacking midfielder
        'ST': {'default_top': 125},  # Forward
        # Add more positions and their default top values as needed
    }

    dot_positions = []
    for position in player_pos.all():
        if position.name[-1] in ['R', 'L', 'C']:  # Check the last letter for position indicator
            position_key = position.name[:-1]  # Extract position key without indicator
            if position_key in position_mapping:
                dot_position = {'left': 250, 'top': position_mapping[position_key]['default_top']}
                if position.name[-1] == 'R':
                    dot_position['left'] = 425  # Value for Right
                elif position.name[-1] == 'L':
                    dot_position['left'] = 75  # Value for Left
                elif position.name[-1] == 'C':
                    dot_position['left'] = 250  # Value for Center
                dot_positions.append(dot_position)
        else:
            dot_positions.append({'left': 250, 'top': position_mapping[position.name]['default_top']})
            

         
    return dot_positions



def get_player_positions(player_pos):
    name_positions = []
    for position_with_spec in player_pos.split(","):
        positions, spec = position_with_spec.split('(') if '(' in position_with_spec else (position_with_spec.strip(), None)
        positions = positions.strip().split('/')
        if spec:
            spec = spec.strip()
        for position in positions:
            position = position.strip()
            if spec:
                for char in spec:
                    if char == 'R':
                        name_positions.append(position + 'R')
                    elif char == 'L':
                        name_positions.append(position + 'L')
                    elif char == 'C':
                        name_positions.append(position + 'C')
            else: #If the position is not specified (case of GK)
                name_positions.append(position)
    return name_positions

def get_player_stats(player, position_name):
    stats = {}
    stats[player.Name] = {}

    for attribute_list in stats_position_dictionary[position_name]:
        attribute_display_name = attribute_list['displayName']
        attribute_name = attribute_list['attributeName']
        stats[player.Name] [attribute_display_name] = getattr(player, attribute_name)

    return stats

def get_default_stats(player):
    stats = {}

    for attribute_list in stats_position_dictionary['DEFAULT']:
        attribute_display_name = attribute_list['displayName']
        attribute_name = attribute_list['attributeName']
        stats[attribute_display_name] = getattr(player, attribute_name)

    return stats

def get_default_avg_stats(position_name):
    stats = {}
    
    position = Position.objects.get(name=position_name)
    players = Player.objects.filter(Pos=position)

    stats['DEFAULT'] = {}

    # Iterating over the attributes defined in the dictionary
    for attribute_list in stats_position_dictionary['DEFAULT']:
        attribute_display_name = attribute_list['displayName']
        attribute_name = attribute_list['attributeName']
        
        # Calculating average, maximum, and minimum for each attribute
        avg_value = players.aggregate(Avg(attribute_name))[f"{attribute_name}__avg"] or 0
        max_value = players.aggregate(Max(attribute_name))[f"{attribute_name}__max"] or 0
        min_value = players.aggregate(Min(attribute_name))[f"{attribute_name}__min"] or 0
        
        rounded_avg_value = round(avg_value, 2)
        rounded_max_value = round(max_value, 2)
        rounded_min_value = round(min_value, 2)
        
        # Storing avg, max, and min values in the stats dictionary
        stats['DEFAULT'][attribute_display_name] = {
            'avg': rounded_avg_value,
            'max': rounded_max_value,
            'min': rounded_min_value,
            'attribute_name': attribute_name  # Add attribute name to the dictionary
        }

    return stats

def get_pos_stats(position_name):
    stats = {}
    
    position = Position.objects.get(name=position_name)
    players = Player.objects.filter(Pos=position)

    stats[position_name] = {}

    # Iterating over the attributes defined in the dictionary
    for attribute_list in stats_position_dictionary[position_name]:
        attribute_display_name = attribute_list['displayName']
        attribute_name = attribute_list['attributeName']
        
        # Calculating average, maximum, and minimum for each attribute
        avg_value = players.aggregate(Avg(attribute_name))[f"{attribute_name}__avg"] or 0
        max_value = players.aggregate(Max(attribute_name))[f"{attribute_name}__max"] or 0
        min_value = players.aggregate(Min(attribute_name))[f"{attribute_name}__min"] or 0
        
        rounded_avg_value = round(avg_value, 2)
        rounded_max_value = round(max_value, 2)
        rounded_min_value = round(min_value, 2)
        
        # Storing avg, max, and min values in the stats dictionary
        stats[position_name][attribute_display_name] = {
            'avg': rounded_avg_value,
            'max': rounded_max_value,
            'min': rounded_min_value,
            'attribute_name': attribute_name  # Add attribute name to the dictionary

        }

    return stats



def get_squad_players(squad_id):
    try:
        squad = Squad.objects.get(id=squad_id)
        players = squad.players.all()
        return players
    except Squad.DoesNotExist:
        return []
    
def search_players_by_positions(players, positions):
    filtered_players = players

    # Ensure positions is a list
    if not isinstance(positions, list):
        positions = [positions]

    print (positions)
    # Filter players by positions
    if positions:
        position_filters = Q()
        for position in positions:
            position_filters |= Q(Pos__name=position)
        filtered_players = filtered_players.filter(position_filters)

    print(filtered_players)
    player_names = [player.Name for player in filtered_players]

    return player_names

import requests

def get_transfermarkt_market_value(player_name):
    url = f'https://transfermarkt-api.vercel.app/players/search/{player_name}?page_number=1'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and data['results']:
            market_value = data['results'][0].get('marketValue', 'Unknown')
            return parse_market_value(market_value)
    return 'Unknown'

def parse_market_value(market_value):
    if market_value == 'Unknown':
        return market_value

    if market_value.endswith('m'):
        value = float(market_value[1:-1].replace(',', ''))  # Remove euro symbol and 'm', replace commas
        return value
    elif market_value.endswith('k'):
        value = float(market_value[1:-1].replace(',', '')) / 1000  # Remove euro symbol and 'k', replace commas, divide by 1000
        return value
    else:
        return 'Unknown'

def get_squad_stats(avg_stats, avg_default_stats, position, players):
    # Dictionary to store statistics and comparisons
    stats = {}
    stats[position] = {}
    stats['DEFAULT'] = {}  # Initialize the 'DEFAULT' key

    # Iterate over each player
    for player in players:
        player_stats = {}

        # Compare player stats with average for position specific stats
        for attribute_display_name, attribute_info in avg_stats[position].items():
            attribute_name = attribute_info['attribute_name']  # Access attribute name
            avg_stat_value = attribute_info['avg']

            player_stat_value = getattr(player, attribute_name)

            # Compare player's stat with average
            if player_stat_value > avg_stat_value:
                comparison = "above average"
            elif player_stat_value < avg_stat_value:
                comparison = "below average"
            else:
                comparison = "equal to average"

            # Check if the player's stat is the maximum or minimum
            is_max = player_stat_value == attribute_info['max']
            is_min = player_stat_value == attribute_info['min']

            player_stats[attribute_display_name] = {
                'value': player_stat_value,
                'comparison': comparison,
                'is_max': is_max,
                'is_min': is_min
            }

        stats[position][player.Name] = player_stats

    # Compare player stats with average for default stats
    for player in players:
        player_stats = {}

        # Compare player stats with average for default stats
        for attribute_display_name, attribute_info in avg_default_stats['DEFAULT'].items():
            attribute_name = attribute_info['attribute_name']  # Access attribute name
            avg_stat_value = attribute_info['avg']

            player_stat_value = getattr(player, attribute_name)

            # Compare player's stat with average
            if player_stat_value > avg_stat_value:
                comparison = "above average"
            elif player_stat_value < avg_stat_value:
                comparison = "below average"
            else:
                comparison = "equal to average"

            # Check if the player's stat is the maximum or minimum
            is_max = player_stat_value == attribute_info['max']
            is_min = player_stat_value == attribute_info['min']

            player_stats[attribute_display_name] = {
                'value': player_stat_value,
                'comparison': comparison,
                'is_max': is_max,
                'is_min': is_min
            }

        stats['DEFAULT'][player.Name] = player_stats

    return stats


def get_max_min_attribute (attribute_name):
    players = Player.objects.all()

    max_value = players.aggregate(Max(attribute_name))[f"{attribute_name}__max"] or 0
    min_value = players.aggregate(Min(attribute_name))[f"{attribute_name}__min"] or 0

    return max_value, min_value

