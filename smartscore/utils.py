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
        if position.name[:2] in position_mapping:
            dot_position = {'left': 250, 'top': position_mapping[position.name[:2]]['default_top']}            
            if position.name[-1]   == 'R':
                dot_position['left'] = 425  # Value for Right
                dot_positions.append(dot_position.copy())
            elif position.name[-1]   == 'L':
                dot_position['left'] = 75  # Value for Left
                dot_positions.append(dot_position.copy())
            elif position.name[-1]   == 'C':
                dot_position['left'] = 250  # Value for Center
                dot_positions.append(dot_position.copy())
            else: #If the position is not specified (case of GK) we add the center dot position
                dot_positions.append(dot_position) 
         
    return dot_positions



#Obtener las posiciones del jugador
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
                        name_positions.append(position + 'D')
                    elif char == 'L':
                        name_positions.append(position + 'I')
                    elif char == 'C':
                        name_positions.append(position + 'C')
            else: #If the position is not specified (case of GK)
                name_positions.append(position)
    return name_positions

#Obtener estadísticas del jugador
def get_player_stats(player):
    
    ataque = (player.xG) + (player.Gol_90 * 15) + (player.Asis_90 *10)
    defensa =  (player.Tackles_won_rat * 15) + (player.Rob_90 * 15)
    pase = (player.Pas_Clv_90 * 10) + (player.Pass_rat * 15) 

    stats = {
        'Ataque': ataque,
        'Defensa': defensa,
        'Pase': pase
    }

    return stats
