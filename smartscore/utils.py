from django.db.models import Avg, Max, Min
from .models import Player, Position, Squad
from .dictionary import stats_position_dictionary

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
            'min': rounded_min_value
        }

    return stats



def get_squad_players(squad_id):
    try:
        squad = Squad.objects.get(id=squad_id)
        players = squad.players.all()
        return players
    except Squad.DoesNotExist:
        return []

