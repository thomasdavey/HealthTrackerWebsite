from users.models import WeightGoal


def bmi(weight, height):
    height = height/100
    bmi = weight / (height*height)
    return bmi


def idealweight(height, sex):
    height = height*0.393701

    if (sex == 'F'):
        idealWeight = 45.5 + ((height - 60) * 2.3)
    elif (sex == 'M'):
        idealWeight = 50 + ((height - 60) * 2.3)

    return idealWeight


def metabolicrate(weight, height, age):
    metabolicRate = (10*weight) + (6.25*height) - (5*age) - 161
    return metabolicRate


def dailycals(metabolicRate, energyExpenditure):
    dailyCals = metabolicRate*energyExpenditure
    return dailyCals


def targetcalories(metabolicRate, energyExpenditure, extremity):
    dailyCals = dailycals(metabolicRate, energyExpenditure)
    calorieDeficit = dailyCals*(-(extremity/10))
    targetCalories = dailyCals - calorieDeficit
    return targetCalories


def targetbreakfast(targetCalories):
    targetBreakfast = targetCalories*0.18
    return targetBreakfast


def targetlunch(targetCalories):
    targetlunch = targetCalories*0.3
    return targetlunch


def targetdinner(targetCalories):
    targetdinner = targetCalories*0.4
    return targetdinner


def targetsnacks(targetCalories):
    targetsnacks = targetCalories*0.12
    return targetsnacks


def netcalories(totalCalories, exerciseCals):
    netCalories = totalCalories - exerciseCals
    return netCalories


def calsunderbudget(targetCalories, netCalories):
    calsUnderBudget = targetCalories - netCalories
    return calsUnderBudget


def targetprotein(weight):
    weight = weight*2.20462
    targetProtein = weight*0.825
    return targetProtein


def targetfat(dailyCals):
    targetfat = (dailyCals*0.25)/9
    return targetfat


def targetcarbs(dailyCals, targetProtein, targetFat):
    targetCarbs = (dailyCals - ((targetProtein*4) + (targetFat*9)))/4
    return targetCarbs


def get_weight_loss_extremity(goal):
    #needs actual method body adding to it
    extremity = 0
    return extremity