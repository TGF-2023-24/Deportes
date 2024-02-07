def get_dot_positions(player_pos):
    dot_positions = []
    for position in player_pos.split(","):
        if 'D' in position or 'I' in position or 'C' in position:
            if 'D' in position:
                if 'I' in position:
                    dot_positions.extend([{'left': 100, 'top': 100}, {'left': 250, 'top': 100}])  # Example positions for right and left
                elif 'C' in position:
                    dot_positions.extend([{'left': 250, 'top': 100}, {'left': 300, 'top': 100}])  # Example positions for right and middle
                else:
                    dot_positions.append({'left': 250, 'top': 100})  # Example position for right
            if 'I' in position and 'D' not in position:
                if 'C' in position:
                    dot_positions.extend([{'left': 100, 'top': 100}, {'left': 200, 'top': 100}])  # Example positions for left and middle
                else:
                    dot_positions.append({'left': 100, 'top': 100})  # Example position for left
            if 'C' in position and 'D' not in position and 'I' not in position:
                dot_positions.append({'left': 250, 'top': 100})  # Example position for middle
        else:
            if position == 'POR':
                dot_positions.append({'left': 250, 'top': 10})  # Example position for goalkeeper
            elif position == 'DF':
                dot_positions.append({'left': 250, 'top': 100})  # Example position for defender
            elif position == 'MC':
                dot_positions.append({'left': 250, 'top': 250})  # Example position for defensive midfielder
            elif position == 'ME':
                dot_positions.append({'left': 250, 'top': 400})  # Example position for midfielder
            elif position == 'MP':
                dot_positions.append({'left': 250, 'top': 550})  # Example position for attacking midfielder
            elif position == 'DL':
                dot_positions.append({'left': 250, 'top': 700})  # Example position for forward
    return dot_positions
