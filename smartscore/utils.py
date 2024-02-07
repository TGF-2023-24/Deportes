def get_dot_positions(player_pos):
    position_mapping = {
        'POR': {'default_top': 750},  # Goalkeeper
        'DF': {'default_top': 650},  # Defender
        'CR': {'default_top': 525},  # Wing-back
        'MC': {'default_top': 525},  # Defensive midfielder
        'ME': {'default_top': 400},  # Midfielder
        'MP': {'default_top': 250},  # Attacking midfielder
        'DL': {'default_top': 125},  # Forward
        # Add more positions and their default top values as needed
    }

    dot_positions = []
    for position_with_spec in player_pos.split(","):
        positions, spec = position_with_spec.split('(') if '(' in position_with_spec else (position_with_spec.strip(), None)
        positions = positions.strip().split('/')
        if spec:
            spec = spec.strip()
        for position in positions:
            position = position.strip()
            if position in position_mapping:
                dot_position = {'left': 250, 'top': position_mapping[position]['default_top']}
                if spec:
                    for char in spec:
                        if char == 'D':
                            dot_position['left'] = 425  # Example value for 'D'
                            dot_positions.append(dot_position.copy())
                        elif char == 'I':
                            dot_position['left'] = 75  # Example value for 'I'
                            dot_positions.append(dot_position.copy())
                        elif char == 'C':
                            dot_position['left'] = 250  # Example value for 'C'
                            dot_positions.append(dot_position.copy())
                else:
                    dot_positions.append(dot_position)
    return dot_positions