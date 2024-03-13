from django.db.models import Avg, Max, Min, Q
from .models import Player, Position, Squad
from .dictionary import stats_position_dictionary
import requests
import numpy as np

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

        # Calculating 70th and 30th percentiles for each attribute
        values = players.values_list(attribute_name, flat=True)
        percentile_70 = np.percentile(values, 70)
        percentile_30 = np.percentile(values, 30)
        percentile_95 = np.percentile(values, 95)
        percentile_5 = np.percentile(values, 5)
        
        rounded_avg_value = round(avg_value, 2)
        rounded_max_value = round(max_value, 2)
        rounded_min_value = round(min_value, 2)
        rounded_percentile_70 = round(percentile_70, 2)
        rounded_percentile_30 = round(percentile_30, 2)
        rounded_percentile_95 = round(percentile_95, 2)
        rounded_percentile_5 = round(percentile_5, 2)
        
        # Storing avg, max, and min values in the stats dictionary
        stats[position_name][attribute_display_name] = {
            'avg': rounded_avg_value,
            'max': rounded_max_value,
            'min': rounded_min_value,
            'percentile_70': rounded_percentile_70,
            'percentile_30': rounded_percentile_30,
            'percentile_95': rounded_percentile_95,
            'percentile_5': rounded_percentile_5,
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

    return filtered_players

import requests

def get_transfermarkt_market_value(player_name):
    #url = f'https://transfermarkt-api.vercel.app/players/search/{player_name}?page_number=1'  
    url = f'http://localhost:8000/players/search/{player_name}?page_number=1'  #when running api on local (no limit on requests)

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
            min_stat_value = attribute_info['min']
            max_stat_value = attribute_info['max']
            percentile70_stat_value = attribute_info['percentile_70']
            percentile30_stat_value = attribute_info['percentile_30']
            percentile95_stat_value = attribute_info['percentile_95']
            percentile5_stat_value = attribute_info['percentile_5']

            player_stat_value = getattr(player, attribute_name)

            # Determine if the player's stat is significantly above or below average
            if player_stat_value >= percentile70_stat_value:
                comparison = "significantly above average"
                if player_stat_value >= percentile95_stat_value:
                    comparison = "exceptional"
            elif player_stat_value <= percentile30_stat_value:
                comparison = "significantly below average"
                if player_stat_value <= percentile5_stat_value:
                    comparison = "horrible"
            else:
                comparison = "average" #The player is mid for this attribute

            # Check if the player's stat is the maximum or minimum
            is_max = player_stat_value == max_stat_value
            is_min = player_stat_value == min_stat_value

            player_stats[attribute_display_name] = {
                'value': player_stat_value,
                'comparison': comparison,
                'is_max': is_max,
                'is_min': is_min
            }

        stats[position][player.Name] = player_stats

    if position == "": #If the position is not specified, we use the default stats
        # Compare player stats with average for default stats
        for player in players:
            player_stats = {}

            # Compare player stats with average for default stats
            for attribute_display_name, attribute_info in avg_default_stats['DEFAULT'].items():
                attribute_name = attribute_info['attribute_name']  # Access attribute name
                avg_stat_value = attribute_info['avg']
                # Check if the player's stat is the maximum or minimum
                is_max = player_stat_value == attribute_info['max']
                is_min = player_stat_value == attribute_info['min']
                percentile70_stat_value = attribute_info['percentile_70']
                percentile30_stat_value = attribute_info['percentile_30']

                player_stat_value = getattr(player, attribute_name)

                # Determine if the player's stat is significantly above or below average
                if player_stat_value >= percentile70_stat_value:
                    comparison = "significantly above average"
                elif player_stat_value <= percentile30_stat_value:
                    comparison = "significantly below average"
                else:
                    comparison = "average" #The player is mid for this attribute
                

                player_stats[attribute_display_name] = {
                    'value': player_stat_value,
                    'comparison': comparison,
                    'is_max': is_max,
                    'is_min': is_min
                }

            stats['DEFAULT'][player.Name] = player_stats

    return stats


def get_max_min_attribute (attribute_name, pos):
    position = Position.objects.get(name=pos)
    players = Player.objects.filter(Pos=position)

    max_value = players.aggregate(Max(attribute_name))[f"{attribute_name}__max"] or 0
    min_value = players.aggregate(Min(attribute_name))[f"{attribute_name}__min"] or 0

    return max_value, min_value

def get_better_players(playerToReplace, players, position):
    better_players = []
    print(f"Player to replace is {playerToReplace.Name}")
    print(f"Position is {position}")
    print(f"Players are {players}")
    playerToReplace_stats = get_player_stats(playerToReplace, position)
    for player in players:
        # We compare each of the player's atrributes for the position
        player_stats = get_player_stats(player, position)
        headToHead = 0
        for attribute in player_stats[player.Name]:
            if player_stats[player.Name][attribute] > playerToReplace_stats[playerToReplace.Name][attribute]:
                headToHead += 1
            elif player_stats[player.Name][attribute] < playerToReplace_stats[playerToReplace.Name][attribute]:
                headToHead -= 1
        if headToHead > 0:
            better_players.append(player)
    return better_players


def smartscore_attributes(player, pos, league, position_weights):
    # Get the position object
    position = Position.objects.get(name=pos)
    
    # Filter players by position
    players = Player.objects.filter(Pos=position)
    
    # Optionally, filter players by league
    if league:
        players = players.filter(League=league)
    
    # Initialize smart score
    smart_score = 0

    print(position_weights)
    
    # Iterate over attribute weights
    for attribute, weight in position_weights.items():
        # Skip attributes with no weight
        if weight == 0:
            continue
        
        # Get the attribute value from the player's profile
        value = getattr(player, attribute)
        
        # Calculate percentile for the attribute
        percentile = get_threshold_attribute(attribute, value, players)
        
        # Calculate attribute weighted score
        smart_score += percentile * weight

    return smart_score


def get_threshold_attribute(attribute_name, player_value, players):
    #If player value not greater than 0, return 0
    if player_value == 0:
        return 0
    # Get the attribute values of all players
    attribute_values = players.values_list(attribute_name, flat=True)

    if not attribute_values:
        attribute_values = [0]
    
    # Convert queryset to numpy array
    attribute_values = np.array(list(attribute_values))
    
    # Calculate the percentile rank of the player's value
    percentile_rank = np.sum(attribute_values <= player_value) / len(attribute_values) * 100
    
    percentile = round(percentile_rank / 100, 2)

    print(f"Percentile for {attribute_name} with value {player_value} is {percentile}")
    return percentile



def filter_recommendations(positions, attributes, foot):
    players = Player.objects.all()
    # Filter players by positions
    if positions:
        position_filters = Q()
        for position in positions:
            position_filters |= Q(Pos__name=position)
        players = players.filter(position_filters)
    print ("Players after position filter: ", players)

    # Filter players by foot
    if foot:
        foot_players = players.filter(Pref_foot=foot)
    else:
        foot_players = players

    print ("Players after foot filter: ", foot_players)
    # For each of the attributes, get its 70th percentile and store it in a dictionary
    print ("Attributes: ", attributes)
    if len(attributes) > 0 and attributes[0] != '':
        attribute_percentiles = {}
        print("We are here")
        for attribute in attributes:
            values = players.values_list(attribute, flat=True)
            percentile_70 = np.percentile(values, 70)
            # Store the 70th percentile in a dictionary
            attribute_percentiles[attribute] = percentile_70

        ok_players = []
        for player in foot_players:
            ok = True
            for attribute in attributes:
                if getattr(player, attribute) < attribute_percentiles[attribute]:
                    ok = False
            if ok:
                ok_players.append(player)
    else:
        ok_players = foot_players

    # Now, we filter the players

    print ("Players after attribute filter: ", ok_players)
    players = list(set(ok_players))
    
    return players

    
    



    
