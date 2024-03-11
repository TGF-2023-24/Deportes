from .utils import get_threshold_attribute
import math

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
        # Define attributes for DL position, total = 50
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
        'Key_hdr_90': 4,
        'Blocks_90': 3,
        'Clr_90': 3,
        'Int_90': 5,
        'Hdr_rat': 3,
        'Tackles_rat': 4,
        'Gl_mistake': -10,
        'Pass_rat': 3,
        'Pr_pass_90': 3,
        'Key_pass_90': 3,
        'Cr_c_90': 3,
        'Cr_c_acc': 3,
        'Ch_c_90': 3,
        'Drb_90': 3,
        'Poss_lost_90': -5,
        'Shot_rat': 1,
        'Conv_rat': 1
    },
    'DR': {
        # Define attributes for DR position
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
        'Key_hdr_90': 4,
        'Blocks_90': 3,
        'Clr_90': 3,
        'Int_90': 5,
        'Hdr_rat': 3,
        'Tackles_rat': 4,
        'Gl_mistake': -10,
        'Pass_rat': 3,
        'Pr_pass_90': 3,
        'Key_pass_90': 3,
        'Cr_c_90': 3,
        'Cr_c_acc': 3,
        'Ch_c_90': 3,
        'Drb_90': 3,
        'Poss_lost_90': -5,
        'Shot_rat': 1,
        'Conv_rat': 1
    },
    'DM': {
        # Define attributes for DM position, total = 50
        'International_match': 2,
        'CAbil': 4,
        'Pot_abil': 6,
        'Strater_match': 3,
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
        'Yel': -5,
        'Red': -10,
        'Dist_90': 5,
        'Key_tck_90': 5,
        'Key_hdr_90': 5,
        'Blocks_90': 5,
        'Clr_90': 4,
        'Int_90': 5,
        'Hdr_rat': 4,
        'Tackles_rat': 5,
        'Gl_mistake': -8,
        'Pass_rat': 5,
        'Pr_pass_90': 3,
        'Key_pass_90': 2,
        'Cr_c_90': 1,
        'Cr_c_acc': 1,
        'Ch_c_90': 1,
        'Drb_90': 1,
        'Poss_lost_90': -6,
        'Shot_rat': 1,
        'Conv_rat': 1
    },
    'WBL': {
        # Define attributes for WBL position, total = 50
        'International_match': 2,
        'CAbil': 4,
        'Pot_abil': 6,
        'Strater_match': 3,
        'Res_match': 1,
        'Min': 3,
        'Goal': 1,
        'Asis': 4,
        'xG': 1,
        'Gol_90': 1,
        'Asis_90': 4,
        'Goal_allowed': 0,
        'Clean_sheet': 0,
        'Sv_rat': 0,
        'xSv_rat': 0,
        'Pen_saved_rat': 0,
        'Faga': 2,
        'Fcomm': -4,
        'Yel': -6,
        'Red': -10,
        'Dist_90': 4,
        'Key_tck_90': 4,
        'Key_hdr_90': 2,
        'Blocks_90': 3,
        'Clr_90': 3,
        'Int_90': 4,
        'Hdr_rat': 2,
        'Tackles_rat': 3,
        'Gl_mistake': -8,
        'Pass_rat': 3,
        'Pr_pass_90': 3,
        'Key_pass_90': 4,
        'Cr_c_90': 4,
        'Cr_c_acc': 4,
        'Ch_c_90': 4,
        'Drb_90': 3,
        'Poss_lost_90': -6,
        'Shot_rat': 1,
        'Conv_rat': 1
    },
    'WBR': {
        # Define attributes for WBR position
        'International_match': 2,
        'CAbil': 4,
        'Pot_abil': 6,
        'Strater_match': 3,
        'Res_match': 1,
        'Min': 3,
        'Goal': 1,
        'Asis': 4,
        'xG': 1,
        'Gol_90': 1,
        'Asis_90': 4,
        'Goal_allowed': 0,
        'Clean_sheet': 0,
        'Sv_rat': 0,
        'xSv_rat': 0,
        'Pen_saved_rat': 0,
        'Faga': 2,
        'Fcomm': -4,
        'Yel': -6,
        'Red': -10,
        'Dist_90': 4,
        'Key_tck_90': 4,
        'Key_hdr_90': 2,
        'Blocks_90': 3,
        'Clr_90': 3,
        'Int_90': 4,
        'Hdr_rat': 2,
        'Tackles_rat': 3,
        'Gl_mistake': -8,
        'Pass_rat': 3,
        'Pr_pass_90': 3,
        'Key_pass_90': 4,
        'Cr_c_90': 4,
        'Cr_c_acc': 4,
        'Ch_c_90': 4,
        'Drb_90': 3,
        'Poss_lost_90': -6,
        'Shot_rat': 1,
        'Conv_rat': 1
    },
    'MC': {
        # Define attributes for MC position, total = 50
        'International_match': 2,
        'CAbil': 4,
        'Pot_abil': 6,
        'Strater_match': 3,
        'Res_match': 1,
        'Min': 3,
        'Goal': 2,
        'Asis': 3,
        'xG': 2,
        'Gol_90': 2,
        'Asis_90': 3,
        'Goal_allowed': 0,
        'Clean_sheet': 0,
        'Sv_rat': 0,
        'xSv_rat': 0,
        'Pen_saved_rat': 0,
        'Faga': 2,
        'Fcomm': -4,
        'Yel': -4,
        'Red': -10,
        'Dist_90': 4,
        'Key_tck_90': 3,
        'Key_hdr_90': 2,
        'Blocks_90': 2,
        'Clr_90': 2,
        'Int_90': 4,
        'Hdr_rat': 2,
        'Tackles_rat': 2,
        'Gl_mistake': -8,
        'Pass_rat': 5,
        'Pr_pass_90': 5,
        'Key_pass_90': 5,
        'Cr_c_90': 2,
        'Cr_c_acc': 2,
        'Ch_c_90': 2,
        'Drb_90': 3,
        'Poss_lost_90': -6,
        'Shot_rat': 2,
        'Conv_rat': 2
    },
    'ML': {
        # Define attributes for ML position, total = 50
        'International_match': 2,
        'CAbil': 4,
        'Pot_abil': 6,
        'Strater_match': 3,
        'Res_match': 1,
        'Min': 3,
        'Goal': 3,
        'Asis': 4,
        'xG': 3,
        'Gol_90': 3,
        'Asis_90': 4,
        'Goal_allowed': 0,
        'Clean_sheet': 0,
        'Sv_rat': 0,
        'xSv_rat': 0,
        'Pen_saved_rat': 0,
        'Faga': 3,
        'Fcomm': -2,
        'Yel': -4,
        'Red': -10,
        'Dist_90': 4,
        'Key_tck_90': 2,
        'Key_hdr_90': 2,
        'Blocks_90': 2,
        'Clr_90': 1,
        'Int_90': 3,
        'Hdr_rat': 1,
        'Tackles_rat': 1,
        'Gl_mistake': -6,
        'Pass_rat': 4,
        'Pr_pass_90': 3,
        'Key_pass_90': 3,
        'Cr_c_90': 3,
        'Cr_c_acc': 3,
        'Ch_c_90': 3,
        'Drb_90': 3,
        'Poss_lost_90': -7,
        'Shot_rat': 2,
        'Conv_rat': 2
    },
    'MR': {
        # Define attributes for MR position
        'International_match': 2,
        'CAbil': 4,
        'Pot_abil': 6,
        'Strater_match': 3,
        'Res_match': 1,
        'Min': 3,
        'Goal': 3,
        'Asis': 4,
        'xG': 3,
        'Gol_90': 3,
        'Asis_90': 4,
        'Goal_allowed': 0,
        'Clean_sheet': 0,
        'Sv_rat': 0,
        'xSv_rat': 0,
        'Pen_saved_rat': 0,
        'Faga': 3,
        'Fcomm': -2,
        'Yel': -4,
        'Red': -10,
        'Dist_90': 4,
        'Key_tck_90': 2,
        'Key_hdr_90': 2,
        'Blocks_90': 2,
        'Clr_90': 1,
        'Int_90': 3,
        'Hdr_rat': 1,
        'Tackles_rat': 1,
        'Gl_mistake': -6,
        'Pass_rat': 4,
        'Pr_pass_90': 3,
        'Key_pass_90': 3,
        'Cr_c_90': 3,
        'Cr_c_acc': 3,
        'Ch_c_90': 3,
        'Drb_90': 3,
        'Poss_lost_90': -7,
        'Shot_rat': 2,
        'Conv_rat': 2
    },
    'AMC': {
        # Define attributes for AMC position, total = 50
        'International_match': 1,
        'CAbil': 4,
        'Pot_abil': 6,
        'Strater_match': 3,
        'Res_match': 1,
        'Min': 3,
        'Goal': 3,
        'Asis': 4,
        'xG': 3,
        'Gol_90': 3,
        'Asis_90': 4,
        'Goal_allowed': 0,
        'Clean_sheet': 0,
        'Sv_rat': 0,
        'xSv_rat': 0,
        'Pen_saved_rat': 0,
        'Faga': 4,
        'Fcomm': -3,
        'Yel': -4,
        'Red': -10,
        'Dist_90': 3,
        'Key_tck_90': 2,
        'Key_hdr_90': 1,
        'Blocks_90': 1,
        'Clr_90': 1,
        'Int_90': 2,
        'Hdr_rat': 1,
        'Tackles_rat': 1,
        'Gl_mistake': -8,
        'Pass_rat': 3,
        'Pr_pass_90': 5,
        'Key_pass_90': 5,
        'Cr_c_90': 2,
        'Cr_c_acc': 2,
        'Ch_c_90': 2,
        'Drb_90': 3,
        'Poss_lost_90': -4,
        'Shot_rat': 3,
        'Conv_rat': 3
    },
    'AML': {
        # Define attributes for AML position, total = 50
        'International_match': 1,
        'CAbil': 4,
        'Pot_abil': 6,
        'Strater_match': 2,
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
        'Faga': 3,
        'Fcomm': -3,
        'Yel': -3,
        'Red': -10,
        'Dist_90': 3,
        'Key_tck_90': 1,
        'Key_hdr_90': 1,
        'Blocks_90': 1,
        'Clr_90': 0,
        'Int_90': 1,
        'Hdr_rat': 1,
        'Tackles_rat': 1,
        'Gl_mistake': -8,
        'Pass_rat': 2,
        'Pr_pass_90': 4,
        'Key_pass_90': 4,
        'Cr_c_90': 3,
        'Cr_c_acc': 3,
        'Ch_c_90': 4,
        'Drb_90': 4,
        'Poss_lost_90': -6,
        'Shot_rat': 2,
        'Conv_rat': 3
    },
    'AMR': {
        # Define attributes for AMR position
        'International_match': 1,
        'CAbil': 4,
        'Pot_abil': 6,
        'Strater_match': 2,
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
        'Faga': 3,
        'Fcomm': -3,
        'Yel': -3,
        'Red': -10,
        'Dist_90': 3,
        'Key_tck_90': 1,
        'Key_hdr_90': 1,
        'Blocks_90': 1,
        'Clr_90': 0,
        'Int_90': 1,
        'Hdr_rat': 1,
        'Tackles_rat': 1,
        'Gl_mistake': -8,
        'Pass_rat': 2,
        'Pr_pass_90': 4,
        'Key_pass_90': 4,
        'Cr_c_90': 3,
        'Cr_c_acc': 3,
        'Ch_c_90': 4,
        'Drb_90': 4,
        'Poss_lost_90': -6,
        'Shot_rat': 2,
        'Conv_rat': 3
    },
    'STC': {
        # Define attributes for STC position, total = 50
        'International_match': 2,
        'CAbil': 4,
        'Pot_abil': 5,
        'Strater_match': 3,
        'Res_match': 1,
        'Min': 3,
        'Goal': 5,
        'Asis': 3,
        'xG': 5,
        'Gol_90': 5,
        'Asis_90': 3,
        'Goal_allowed': 0,
        'Clean_sheet': 0,
        'Sv_rat': 0,
        'xSv_rat': 0,
        'Pen_saved_rat': 0,
        'Faga': 4,
        'Fcomm': -3,
        'Yel': -5,
        'Red': -10,
        'Dist_90': 3,
        'Key_tck_90': 1,
        'Key_hdr_90': 3,
        'Blocks_90': 0,
        'Clr_90': 0,
        'Int_90': 2,
        'Hdr_rat': 3,
        'Tackles_rat': 0,
        'Gl_mistake': -5,
        'Pass_rat': 1,
        'Pr_pass_90': 2,
        'Key_pass_90': 3,
        'Cr_c_90': 1,
        'Cr_c_acc': 1,
        'Ch_c_90': 3,
        'Drb_90': 4,
        'Poss_lost_90': -5,
        'Shot_rat': 4,
        'Conv_rat': 4
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
        percentile = get_threshold_attribute(attribute, pos, league, value)

        print("Attribute: ", attribute, "Percentile: ", percentile, "Weight: ", weight)
        
        smart_score += percentile * weight

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
    
    if budget != 9999: #If budget is defined
        value = getattr(player, 'market_value')
        if value != 'Unknown':
             smart_score *= adjust_for_budget(budget, value) 
       
        
    print("SmartScore final: ", round(smart_score))
    return round(smart_score) #Round to the nearest whole number



def sigmoid(x, a=1, b=0, c=1):
    min_val = 0.9
    """
    Sigmoid function with parameters a, b, and c:
    f(x) = c / (1 + exp(-a*(x-b)))
    """
    return c - (c / (1 + math.exp(-a * (x - b)))) + min_val

def adjust_for_budget(budget, playerValue):
    playerValue = float(playerValue)
    if playerValue > budget:
        return 0.5 #Unaffordable
    budgetFraction = playerValue / budget
    
    # Parameters for the sigmoid function
    a = 10  # Controls the steepness of the curve
    b = 0.2  # Shifts the curve along the x-axis
    c = 0.75  # Maximum value of the curve

    # Calculate the adjustment factor using the sigmoid function
    adjustment_factor = sigmoid(budgetFraction, a=a, b=b, c=c)

    #HAY UN GRÁFICO DE LA CURVA EN LA CARPETA DE IMÁGENES
    print("Budget fraction: ", budgetFraction, "Adjustment factor: ", adjustment_factor)
    
    return adjustment_factor



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
        calculation = pow(abs(age_difference)/12, 7/2) #Only players in the extremes will be affected
    elif growth_factor == 2:
        calculation = pow(abs(age_difference)/10, 2) #Players in the extremes will be affected, others will be affected less
        calculation = round(calculation, 2)
    if age_difference < 0:
        # Player is younger than the threshold, give a bonus
        score += calculation
    else:
        # Player is older than the threshold, penalize
        score -= calculation

    return score


def adjust_for_budget_antiguo(budget, playerValue):
    print("Player value: ", playerValue, "Budget: ", budget)
    playerValue = float(playerValue)
    # Adjust score based on budget
    if playerValue > budget:
        return 0.5 #Unaffordable
    budgetFraction = playerValue / budget
    if budgetFraction < 0.1:
        factor = 1.25 #Cheap signing
    elif 0.1 <= budgetFraction < 0.25:
        factor = 1.15 #Good value
    elif 0.25 <= budgetFraction < 0.35:
        factor = 1.07 #Fair value
    elif 0.35 <= budgetFraction < 0.5:
        factor = 1.03 #Important signing
    elif 0.5 <= budgetFraction < 0.75:
        factor = 1 #Expensive signing
    else:
        return 0.9 #Very expensive signing
    
    return pow(factor, 2)