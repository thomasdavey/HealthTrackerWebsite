from datetime import date

def bmi(weight, height):
    height = height/100
    bmi = weight / (height*height)
    return bmi



def ideal_weight(height, sex):
    height = height*0.393701

    if (sex == 'F'):
        ideal_weight = 45.5 + ((height - 60) * 2.3)
    elif (sex == 'M'):
        ideal_weight = 50 + ((height - 60) * 2.3)

    return ideal_weight


def metabolic_rate(weight, height, age):
    metabolic_rate = (10*weight) + (6.25*height) - (5*age) - 161
    return metabolic_rate


def daily_cal(metabolic, energy):
    daily_cals = float(metabolic) * float(energy)
    return int(daily_cals)


def target_calories(metabolic, energy, extremity):
    daily_cals = daily_cal(metabolic, energy)
    calorie_deficit = daily_cals*(-(extremity/10))
    target_calories = daily_cals - calorie_deficit
    return int(target_calories)


def target_breakfast(target_calories):
    target_breakfast = target_calories*0.18
    return target_breakfast


def target_lunch(target_calories):
    target_lunch = target_calories*0.3
    return target_lunch


def target_dinner(target_calories):
    target_dinner = target_calories*0.4
    return target_dinner


def target_snacks(target_calories):
    target_snacks = target_calories*0.12
    return target_snacks


def net_calories(total_calories, exercise_cals):
    net_cals = int(total_calories) - int(exercise_cals)
    return net_cals


def cals_under_budget(target_calories, net_calories):
    cals_under_budget = int(target_calories) - int(net_calories)
    return cals_under_budget


def target_protein(weight):
    weight = weight*2.20462
    target_protein = weight*0.825
    return target_protein


def target_fat(daily_cals):
    target_fat = (daily_cals*0.25)/9
    return target_fat


def target_carbs(daily_cals, target_protein, target_fat):
    target_carbs = (daily_cals - ((target_protein*4) + (target_fat*9)))/4
    return target_carbs


def get_weight_loss_extremity(user):
    weight_loss = int(user.profile.weight - user.weightgoal.target_weight)
    days_between = user.weightgoal.target_date - date.today()
    num_weeks = int(days_between.days) / 7
    kg_per_week = weight_loss / num_weeks
    if kg_per_week > -3 and kg_per_week < -2:
        extremity = 3;

    elif kg_per_week > -2 and kg_per_week < -1:
        extremity = 2;

    elif kg_per_week > -1 and kg_per_week <= 0:
        extremity = 1;

    elif kg_per_week > 0 and kg_per_week < 1:
        extremity = -1;

    elif kg_per_week > 1 and kg_per_week < 2:
        extremity = -2;

    elif kg_per_week > 2 and kg_per_week < 3:
        extremity = -3;

    else:
        print("Please set a different goal. This goal is too difficult to acheive within the time limit.")

    return extremity


