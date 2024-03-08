from .utils import get_threshold_attribute

position_weights = {
    'GK': { #Total = 50
        'International_match': 5,
        'CAbil': 4,
        'Pot_abil': 6,
        'Strater_match': 5,
        'Res_match': 0,
        'Min': 0,
        'Goal': 0,
        'Asis': 1,
        'xG': 0,
        'Gol_90': 0,
        'Asis_90': 1,
        'Goal_allowed': -7,
        'Clean_sheet': 10,
        'Sv_rat': 6,
        'xSv_rat': 6,
        'Pen_saved_rat': 5,
        'Faga': 1,
        'Fcomm': -3,
        'Yel': -3,
        'Red': -8,
        'Dist_90': 0,
        'Key_tck_90': 4,
        'Key_hdr_90': 4,
        'Blocks_90': 3,
        'Clr_90': 5,
        'Int_90': 4,
        'Hdr_rat': 2,
        'Tackles_rat': 2,
        'Gl_mistake': -9,
        'Pass_rat': 5,
        'Pr_pass_90': 2,
        'Key_pass_90': 2,
        'Cr_c_90': 0,
        'Cr_c_acc': 0,
        'Ch_c_90': 0,
        'Drb_90': 0,
        'Poss_lost_90': -3,
        'Shot_rat': 0,
        'Conv_rat': 0
    },
    'DC': {
        # Define attributes for DC position, total = 50
        'International_match': 2,
        'CAbil': 4,
        'Pot_abil': 6,
        'Strater_match': 3,
        'Res_match': 0,
        'Min': 3,
        'Goal': 1,
        'Asis': 2,
        'xG': 1,
        'Gol_90': 1,
        'Asis_90': 3,
        'Goal_allowed': 0,
        'Clean_sheet': 0,
        'Sv_rat': 0,
        'xSv_rat': 0,
        'Pen_saved_rat': 0,
        'Faga': 1,
        'Fcomm': -4,
        'Yel': -5,
        'Red': -10,
        'Dist_90': 4,
        'Key_tck_90': 6,
        'Key_hdr_90': 6,
        'Blocks_90': 5,
        'Clr_90': 5,
        'Int_90': 6,
        'Hdr_rat': 5,
        'Tackles_rat': 5,
        'Gl_mistake': -9,
        'Pass_rat': 5,
        'Pr_pass_90': 3,
        'Key_pass_90': 1,
        'Cr_c_90': 1,
        'Cr_c_acc': 1,
        'Ch_c_90': 1,
        'Drb_90': 1,
        'Poss_lost_90': -6,
        'Shot_rat': 1,
        'Conv_rat': 1
    },
    'DL': {
        # Define attributes for DL position
        'International_match': 1,
        'CAbil': 3,
        'Pot_abil': 5,
        'Strater_match': 3,
        'Res_match': 1,
        'Min': 3,
        'Goal': 1,
        'Asis': 5,
        'xG': 1,
        'Gol_90': 1,
        'Asis_90': 5,
        'Goal_allowed': 0,
        'Clean_sheet': 0,
        'Sv_rat': 0,
        'xSv_rat': 0,
        'Pen_saved_rat': 0,
        'Faga': 2,
        'Fcomm': -5,
        'Yel': -5,
        'Red': -10,
        'Dist_90': 5,
        'Key_tck_90': 4,
        'Key_hdr_90': 2,
        'Blocks_90': 3,
        'Clr_90': 3,
        'Int_90': 5,
        'Hdr_rat': 2,
        'Tackles_rat': 4,
        'Gl_mistake': -10,
        'Pass_rat': 3,
        'Pr_pass_90': 3,
        'Key_pass_90': 3,
        'Cr_c_90': 3,
        'Cr_c_acc': 3,
        'Ch_c_90': 3,
        'Drb_90': 2,
        'Poss_lost_90': -5,
        'Shot_rat': 1,
        'Conv_rat': 1
    },
    'DR': {
        # Define attributes for DR position
        'International_match': 3,
        'CAbil': 4,
        'Pot_abil': 6,
        'Strater_match': 4,
        'Res_match': 2,
        'Min': 3,
        'Goal': 2,
        'Asis': 5,
        'xG': 2,
        'Gol_90': 2,
        'Asis_90': 5,
        'Goal_allowed': 0,
        'Clean_sheet': 0,
        'Sv_rat': 0,
        'xSv_rat': 0,
        'Pen_saved_rat': 0,
        'Faga': 2,
        'Fcomm': -5,
        'Yel': -4,
        'Red': -8,
        'Dist_90': 5,
        'Key_tck_90': 5,
        'Key_hdr_90': 3,
        'Blocks_90': 5,
        'Clr_90': 4,
        'Int_90': 6,
        'Hdr_rat': 4,
        'Tackles_rat': 6,
        'Gl_mistake': -8,
        'Pass_rat': 4,
        'Pr_pass_90': 4,
        'Key_pass_90': 4,
        'Cr_c_90': 4,
        'Cr_c_acc': 4,
        'Ch_c_90': 4,
        'Drb_90': 3,
        'Poss_lost_90': -3,
        'Shot_rat': 1,
        'Conv_rat': 1
    },
    'DM': {
        # Define attributes for DM position
        'International_match': 4,
        'CAbil': 4,
        'Pot_abil': 6,
        'Strater_match': 4,
        'Res_match': 1,
        'Min': 3,
        'Goal': 1,
        'Asis': 3,
        'xG': 1,
        'Gol_90': 1,
        'Asis_90': 3,
        'Goal_allowed': 0,
        'Clean_sheet': 0,
        'Sv_rat': 0,
        'xSv_rat': 0,
        'Pen_saved_rat': 0,
        'Faga': 1,
        'Fcomm': -4,
        'Yel': -4,
        'Red': -8,
        'Dist_90': 6,
        'Key_tck_90': 6,
        'Key_hdr_90': 6,
        'Blocks_90': 4,
        'Clr_90': 4,
        'Int_90': 6,
        'Hdr_rat': 5,
        'Tackles_rat': 5,
        'Gl_mistake': -8,
        'Pass_rat': 5,
        'Pr_pass_90': 3,
        'Key_pass_90': 2,
        'Cr_c_90': 2,
        'Cr_c_acc': 2,
        'Ch_c_90': 2,
        'Drb_90': 1,
        'Poss_lost_90': -5,
        'Shot_rat': 1,
        'Conv_rat': 1
    },
    'WBL': {
        # Define attributes for WBL position
        'International_match': 3,
        'CAbil': 4,
        'Pot_abil': 6,
        'Strater_match': 4,
        'Res_match': 2,
        'Min': 3,
        'Goal': 2,
        'Asis': 5,
        'xG': 2,
        'Gol_90': 2,
        'Asis_90': 5,
        'Goal_allowed': 0,
        'Clean_sheet': 0,
        'Sv_rat': 0,
        'xSv_rat': 0,
        'Pen_saved_rat': 0,
        'Faga': 2,
        'Fcomm': -4,
        'Yel': -4,
        'Red': -8,
        'Dist_90': 5,
        'Key_tck_90': 5,
        'Key_hdr_90': 3,
        'Blocks_90': 5,
        'Clr_90': 4,
        'Int_90': 6,
        'Hdr_rat': 4,
        'Tackles_rat': 6,
        'Gl_mistake': -8,
        'Pass_rat': 4,
        'Pr_pass_90': 4,
        'Key_pass_90': 4,
        'Cr_c_90': 4,
        'Cr_c_acc': 4,
        'Ch_c_90': 4,
        'Drb_90': 3,
        'Poss_lost_90': -3,
        'Shot_rat': 1,
        'Conv_rat': 1
    },
    'WBR': {
        # Define attributes for WBR position
        'International_match': 3,
        'CAbil': 4,
        'Pot_abil': 6,
        'Strater_match': 4,
        'Res_match': 2,
        'Min': 3,
        'Goal': 2,
        'Asis': 5,
        'xG': 2,
        'Gol_90': 2,
        'Asis_90': 5,
        'Goal_allowed': 0,
        'Clean_sheet': 0,
        'Sv_rat': 0,
        'xSv_rat': 0,
        'Pen_saved_rat': 0,
        'Faga': 2,
        'Fcomm': -4,
        'Yel': -4,
        'Red': -8,
        'Dist_90': 5,
        'Key_tck_90': 5,
        'Key_hdr_90': 3,
        'Blocks_90': 5,
        'Clr_90': 4,
        'Int_90': 6,
        'Hdr_rat': 4,
        'Tackles_rat': 6,
        'Gl_mistake': -8,
        'Pass_rat': 4,
        'Pr_pass_90': 4,
        'Key_pass_90': 4,
        'Cr_c_90': 4,
        'Cr_c_acc': 4,
        'Ch_c_90': 4,
        'Drb_90': 3,
        'Poss_lost_90': -3,
        'Shot_rat': 1,
        'Conv_rat': 1
    },
    'MC': {
        # Define attributes for MC position
        'International_match': 3,
        'CAbil': 4,
        'Pot_abil': 6,
        'Strater_match': 4,
        'Res_match': 2,
        'Min': 3,
        'Goal': 3,
        'Asis': 5,
        'xG': 3,
        'Gol_90': 3,
        'Asis_90': 5,
        'Goal_allowed': 0,
        'Clean_sheet': 0,
        'Sv_rat': 0,
        'xSv_rat': 0,
        'Pen_saved_rat': 0,
        'Faga': 3,
        'Fcomm': -4,
        'Yel': -3,
        'Red': -7,
        'Dist_90': 5,
        'Key_tck_90': 4,
        'Key_hdr_90': 3,
        'Blocks_90': 4,
        'Clr_90': 3,
        'Int_90': 4,
        'Hdr_rat': 3,
        'Tackles_rat': 3,
        'Gl_mistake': -8,
        'Pass_rat': 6,
        'Pr_pass_90': 5,
        'Key_pass_90': 5,
        'Cr_c_90': 3,
        'Cr_c_acc': 3,
        'Ch_c_90': 3,
        'Drb_90': 3,
        'Poss_lost_90': -4,
        'Shot_rat': 2,
        'Conv_rat': 2
    },
    'ML': {
        # Define attributes for ML position
        'International_match': 3,
        'CAbil': 4,
        'Pot_abil': 6,
        'Strater_match': 4,
        'Res_match': 1,
        'Min': 3,
        'Goal': 4,
        'Asis': 5,
        'xG': 4,
        'Gol_90': 4,
        'Asis_90': 5,
        'Goal_allowed': 0,
        'Clean_sheet': 0,
        'Sv_rat': 0,
        'xSv_rat': 0,
        'Pen_saved_rat': 0,
        'Faga': 4,
        'Fcomm': -2,
        'Yel': -3,
        'Red': -7,
        'Dist_90': 4,
        'Key_tck_90': 3,
        'Key_hdr_90': 3,
        'Blocks_90': 3,
        'Clr_90': 2,
        'Int_90': 4,
        'Hdr_rat': 3,
        'Tackles_rat': 3,
        'Gl_mistake': -6,
        'Pass_rat': 4,
        'Pr_pass_90': 4,
        'Key_pass_90': 4,
        'Cr_c_90': 4,
        'Cr_c_acc': 4,
        'Ch_c_90': 4,
        'Drb_90': 4,
        'Poss_lost_90': -3,
        'Shot_rat': 3,
        'Conv_rat': 3
    },
    'MR': {
        # Define attributes for MR position
        'International_match': 3,
        'CAbil': 4,
        'Pot_abil': 6,
        'Strater_match': 4,
        'Res_match': 1,
        'Min': 3,
        'Goal': 4,
        'Asis': 5,
        'xG': 4,
        'Gol_90': 4,
        'Asis_90': 5,
        'Goal_allowed': 0,
        'Clean_sheet': 0,
        'Sv_rat': 0,
        'xSv_rat': 0,
        'Pen_saved_rat': 0,
        'Faga': 4,
        'Fcomm': -2,
        'Yel': -3,
        'Red': -7,
        'Dist_90': 4,
        'Key_tck_90': 3,
        'Key_hdr_90': 3,
        'Blocks_90': 3,
        'Clr_90': 2,
        'Int_90': 4,
        'Hdr_rat': 3,
        'Tackles_rat': 3,
        'Gl_mistake': -6,
        'Pass_rat': 4,
        'Pr_pass_90': 4,
        'Key_pass_90': 4,
        'Cr_c_90': 4,
        'Cr_c_acc': 4,
        'Ch_c_90': 4,
        'Drb_90': 4,
        'Poss_lost_90': -3,
        'Shot_rat': 3,
        'Conv_rat': 3
    },
    'AMC': {
        # Define attributes for AMC position
        'International_match': 3,
        'CAbil': 4,
        'Pot_abil': 6,
        'Strater_match': 4,
        'Res_match': 2,
        'Min': 3,
        'Goal': 5,
        'Asis': 5,
        'xG': 5,
        'Gol_90': 5,
        'Asis_90': 5,
        'Goal_allowed': -0,
        'Clean_sheet': 0,
        'Sv_rat': 0,
        'xSv_rat': 0,
        'Pen_saved_rat': 0,
        'Faga': 4,
        'Fcomm': -2,
        'Yel': -3,
        'Red': -7,
        'Dist_90': 2,
        'Key_tck_90': 2,
        'Key_hdr_90': 2,
        'Blocks_90': 2,
        'Clr_90': 1,
        'Int_90': 2,
        'Hdr_rat': 2,
        'Tackles_rat': 2,
        'Gl_mistake': -8,
        'Pass_rat': 4,
        'Pr_pass_90': 5,
        'Key_pass_90': 6,
        'Cr_c_90': 4,
        'Cr_c_acc': 4,
        'Ch_c_90': 4,
        'Drb_90': 4,
        'Poss_lost_90': -3,
        'Shot_rat': 3,
        'Conv_rat': 4
    },
    'AML': {
        # Define attributes for AML position
        'International_match': 3,
        'CAbil': 4,
        'Pot_abil': 6,
        'Strater_match': 5,
        'Res_match': 2,
        'Min': 3,
        'Goal': 5,
        'Asis': 5,
        'xG': 5,
        'Gol_90': 5,
        'Asis_90': 5,
        'Goal_allowed': 0,
        'Clean_sheet': 0,
        'Sv_rat': 0,
        'xSv_rat': 0,
        'Pen_saved_rat': 0,
        'Faga': 4,
        'Fcomm': -2,
        'Yel': -3,
        'Red': -7,
        'Dist_90': 3,
        'Key_tck_90': 2,
        'Key_hdr_90': 2,
        'Blocks_90': 1,
        'Clr_90': 1,
        'Int_90': 1,
        'Hdr_rat': 2,
        'Tackles_rat': 2,
        'Gl_mistake': -8,
        'Pass_rat': 2,
        'Pr_pass_90': 4,
        'Key_pass_90': 4,
        'Cr_c_90': 4,
        'Cr_c_acc': 4,
        'Ch_c_90': 4,
        'Drb_90': 4,
        'Poss_lost_90': -3,
        'Shot_rat': 4,
        'Conv_rat': 4
    },
    'AMR': {
        # Define attributes for AMR position
        'International_match': 3,
        'CAbil': 4,
        'Pot_abil': 6,
        'Strater_match': 5,
        'Res_match': 2,
        'Min': 3,
        'Goal': 5,
        'Asis': 5,
        'xG': 5,
        'Gol_90': 5,
        'Asis_90': 5,
        'Goal_allowed': 0,
        'Clean_sheet': 0,
        'Sv_rat': 0,
        'xSv_rat': 0,
        'Pen_saved_rat': 0,
        'Faga': 4,
        'Fcomm': -2,
        'Yel': -3,
        'Red': -7,
        'Dist_90': 3,
        'Key_tck_90': 2,
        'Key_hdr_90': 2,
        'Blocks_90': 1,
        'Clr_90': 1,
        'Int_90': 1,
        'Hdr_rat': 2,
        'Tackles_rat': 2,
        'Gl_mistake': -8,
        'Pass_rat': 2,
        'Pr_pass_90': 4,
        'Key_pass_90': 4,
        'Cr_c_90': 4,
        'Cr_c_acc': 4,
        'Ch_c_90': 4,
        'Drb_90': 4,
        'Poss_lost_90': -3,
        'Shot_rat': 4,
        'Conv_rat': 4
    },
    'STC': {
        'International_match': 4,
        'CAbil': 5,
        'Pot_abil': 5,
        'Strater_match': 4,
        'Res_match': 1,
        'Min': 3,
        'Goal': 5,
        'Asis': 4,
        'xG': 5,
        'Gol_90': 5,
        'Asis_90': 4,
        'Goal_allowed': 0,
        'Clean_sheet': 0,
        'Sv_rat': 0,
        'xSv_rat': 0,
        'Pen_saved_rat': 0,
        'Faga': -3,
        'Fcomm': -3,
        'Yel': -2,
        'Red': -5,
        'Dist_90': 3,
        'Key_tck_90': 2,
        'Key_hdr_90': 4,
        'Blocks_90': 2,
        'Clr_90': 2,
        'Int_90': 2,
        'Hdr_rat': 4,
        'Tackles_rat': 2,
        'Gl_mistake': -4,
        'Pass_rat': 3,
        'Pr_pass_90': 3,
        'Key_pass_90': 4,
        'Cr_c_90': 3,
        'Cr_c_acc': 3,
        'Ch_c_90': 3,
        'Drb_90': 4,
        'Poss_lost_90': -3,
        'Shot_rat': 5,
        'Conv_rat': 5
    }
}


def smartScore(player, pos, budget, expectations, league):
    smart_score = 0
    # Get the weights for the player's position
    weights = position_weights.get(pos)

    for attribute, weight in weights.items():
        if weight == 0:
            continue # Skip attributes with no weight

        # Get the attribute value from the player's profile
        value = getattr(player, attribute)
        percentile = get_threshold_attribute(attribute, pos, "", value)

        print("Attribute: ", attribute, "Percentile: ", percentile, "Weight: ", weight)
        
        smart_score += percentile * weight

    smart_score = round(smart_score, 2)
    print ("Smart Score after attribute weighting: ", smart_score)

    # We want to give a higher score to players with higher potential ability, compared to current ability
    # The greater  the difference between potential ability and current ability, the higher the score (exponential growth)
    projected_growth = (getattr(player, 'Pot_abil') / getattr(player, 'CAbil'))
    print("Projected growth: ", projected_growth)
    smart_score *= pow(projected_growth, 3)
        
    # Threshold is 27 years old, the further away from this age, the higher the penalty or bonus (exponential growth)
    growth_factor = expectations 
    age_score = calculate_age_score(getattr(player, 'Age'), growth_factor)
    smart_score *= age_score

    print("Smart Score after age and potential ability weighting: ", smart_score)

     # Adjust score based on international match experience, reward players with more experience
    int_matches = getattr(player, 'International_match')
    if 0 < int_matches <= 50:
        smart_score *= 1.05
    elif 50 < int_matches <= 150:
        smart_score *= 1.1
    elif int_matches > 150:
        smart_score *= 1.15

    print("Smart Score after international match experience weighting: ", smart_score)
    
    #smart_score *= adjust_for_budget(budget) * adjust_for_expectations(short_term, long_term)

    #tener en cuenta market_value, LIga, equipo?, Contrato?, salario?, partidos int (negativo para equipo + desgaste?) edad, altura peso? (depende posicion?), (pie))?
    return smart_score

def normalize(value, min, max):
    # Normalize value to a range between 0 and 1
    #If they are different from 0
    if min != 0 or max != 0:
        normalized_value = (value - min) / (max - min)
        return normalized_value
    
    return 0

def adjust_for_budget(budget):
    # Adjust score based on budget constraints
    # Implement adjustment logic heres
    pass


def calculate_age_score(age, growth_factor):
    # Grow factor can be adjusted according to the importance of age 
    # Not important: 0
    # Important: 1
    # Very important: 2
    score = 1 
    threshold = 27
    age_difference = age - threshold
    
    if growth_factor == 0:
        # Age is not important
        return score
    elif growth_factor == 1:
        calculation = pow(age_difference/12, 9/2) #Only players in the extremes will be affected
    elif growth_factor == 2:
        calculation = pow(age_difference/10, 5/2) #Players in the extremes will be affected, others will be affected less

    if age_difference < 0:
        # Player is younger than the threshold, give a bonus
        score += calculation
    else:
        # Player is older than the threshold, penalize
        score -= calculation
    
    return score




