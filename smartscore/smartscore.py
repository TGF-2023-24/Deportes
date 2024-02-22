from .utils import get_max_min_attribute

position_weights = {
    'GK': {
        'International_match': 1,
        'CAbil': 5,
        'Pot_abil': 5,
        'Strater_match': 3,
        'Res_match': 3,
        'Min': 2,
        'Goal': 5,
        'Asis': 3,
        'xG': 4,
        'Gol_90': 4,
        'Asis_90': 3,
        'Goal_allowed': -5,
        'Clean_sheet': 5,
        'Sv_rat': 4,
        'xSv_rat': 4,
        'Pen_saved_rat': 5,
        'Faga': -3,
        'Fcomm': -3,
        'Yel': -2,
        'Red': -5,
        'Dist_90': 3,
        'Key_tck_90': 4,
        'Key_hdr_90': 4,
        'Blocks_90': 3,
        'Clr_90': 4,
        'Int_90': 4,
        'Hdr_rat': 4,
        'Tackles_rat': 4,
        'Gl_mistake': -5,
        'Pass_rat': 4,
        'Pr_pass_90': 4,
        'Key_pass_90': 4,
        'Cr_c_90': 3,
        'Cr_c_acc': 3,
        'Ch_c_90': 3,
        'Drb_90': 3,
        'Poss_lost_90': -3,
        'Shot_rat': 4,
        'Conv_rat': 4
    },
    'DC': {
    },
    'DL': {
        # Define attributes for DL position
    },
    'DR': {
        # Define attributes for DR position
    },
    'DM': {
        # Define attributes for DM position
    },
    'WBL': {
        # Define attributes for WBL position
    },
    'WBR': {
        # Define attributes for WBR position
    },
    'MC': {
        # Define attributes for MC position
    },
    'ML': {
        # Define attributes for ML position
    },
    'MR': {
        # Define attributes for MR position
    },
    'AMC': {
        # Define attributes for AMC position
    },
    'AML': {
        # Define attributes for AML position
    },
    'AMR': {
        # Define attributes for AMR position
    },
    'STC': {
        'International_match': 1,
        'CAbil': 5,
        'Pot_abil': 5,
        'Strater_match': 4,
        'Res_match': 3,
        'Min': 4,
        'Goal': 5,
        'Asis': 4,
        'xG': 5,
        'Gol_90': 5,
        'Asis_90': 4,
        'Goal_allowed': -2,
        'Clean_sheet': -3,
        'Sv_rat': -2,
        'xSv_rat': -2,
        'Pen_saved_rat': -2,
        'Faga': -3,
        'Fcomm': -3,
        'Yel': -2,
        'Red': -5,
        'Dist_90': 3,
        'Key_tck_90': 2,
        'Key_hdr_90': 2,
        'Blocks_90': 2,
        'Clr_90': 2,
        'Int_90': 2,
        'Hdr_rat': 2,
        'Tackles_rat': 2,
        'Gl_mistake': -4,
        'Pass_rat': 4,
        'Pr_pass_90': 4,
        'Key_pass_90': 5,
        'Cr_c_90': 5,
        'Cr_c_acc': 4,
        'Ch_c_90': 5,
        'Drb_90': 5,
        'Poss_lost_90': -3,
        'Shot_rat': 5,
        'Conv_rat': 5
    }
}


def smart_score(player, pos, weights, budget, short_term, long_term):
    smart_score = 0

    for attribute, weight in weights.items():
        max, min = get_max_min_attribute(attribute, player.get(pos))
        # Normalize attribute value if necessary
        normalized_value = normalize(player.get(attribute), min, max)
        smart_score += normalized_value * weight
    
    #smart_score *= adjust_for_budget(budget) * adjust_for_expectations(short_term, long_term)

    return smart_score

def normalize(value, min, max):
    # Normalize value to a range between 0 and 1

    normalized_value = (value - min) / (max - min)

    return normalized_value

def adjust_for_budget(budget):
    # Adjust score based on budget constraints
    # Implement adjustment logic here
    pass

def adjust_for_expectations(short_term, long_term):
    # Adjust score based on short-term and long-term expectations
    # Implement adjustment logic here
    pass


