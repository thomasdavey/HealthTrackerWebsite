from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import date
from .models import CalorieCount


class Calculator:
    user = User
    height = 0.0
    weight = 0.0
    sex = ''
    age = 0
    energy = 0.0

    def __init__(self, user):
        today = date.today()
        dob = user.profile.birth_date

        self.user = user
        self.height = user.profile.height
        self.weight = user.profile.weight
        self.sex = user.profile.sex
        self.age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        self.energy = user.profile.activity_level

    def bmi(self):
        h = self.height / 100
        w = self.weight
        return w / (h*h)

    def ideal_weight(self):
        h = self.height * 0.393701
        s = self.sex

        if s == 'M':
            return 50 + ((h - 60) * 2.3)
        else:
            return 45.5 + ((h - 60) * 2.3)

    def metabolic_rate(self):
        h = self.height
        w = self.weight
        a = self.age
        s = self.sex

        if s == 'M':
            return (10*w) + (6.25*h) - (5*a) + 5
        else:
            return (10*w) + (6.25*h) - (5*a) - 161

    def daily_calories(self):
        return int(float(self.metabolic_rate()) * float(self.energy))

    def extremity(self):
        loss = int(self.weight - self.user.weightgoal.target_weight)
        days = self.user.weightgoal.target_date - date.today()
        weeks = int(days.days) / 7
        kg = loss / weeks

        if -3 < kg <= -2:
            return 3
        elif -2 < kg <= -1:
            return 2
        elif -1 < kg <= 0:
            return 1
        elif 0 < kg <= 1:
            return -1
        elif 1 < kg <= 2:
            return -2
        elif 2 < kg <= 3:
            return -3
        else:
            print("Please set a different goal. This goal is too difficult to achieve within the time limit.")

    def target_calories(self):
        deficit = self.daily_calories() * (-(self.extremity()/10))
        return int(self.daily_calories() - deficit)

    def target_breakfast(self):
        return int(self.target_calories() * 0.18)

    def target_lunch(self):
        return int(self.target_calories() * 0.3)

    def target_dinner(self):
        return int(self.target_calories() * 0.4)

    def target_snack(self):
        return int(self.target_calories() * 0.12)

    def target_protein(self):
        return int(self.weight * 2.20462 * 0.825)

    def target_fat(self):
        return int((self.daily_calories()*0.25)/9)

    def target_carbs(self):
        return int((self.daily_calories() - ((self.target_protein()*4) + (self.target_fat()*9)))/4)


class Accessor:
    user = User

    def __init__(self, user):
        self.user = user

    def total_breakfast(self):
        total = CalorieCount.objects.filter(user=self.user, date=date.today(), meal='BF')
        return total.aggregate(Sum('kcals'))['kcals__sum'] or 0

    def total_lunch(self):
        total = CalorieCount.objects.filter(user=self.user, date=date.today(), meal='LU')
        return total.aggregate(Sum('kcals'))['kcals__sum'] or 0

    def total_dinner(self):
        total = CalorieCount.objects.filter(user=self.user, date=date.today(), meal='DN')
        return total.aggregate(Sum('kcals'))['kcals__sum'] or 0

    def total_snacks(self):
        total = CalorieCount.objects.filter(user=self.user, date=date.today(), meal='SK')
        return total.aggregate(Sum('kcals'))['kcals__sum'] or 0

    def total_calories(self):
        return self.total_breakfast() + self.total_lunch() + self.total_dinner() + self.total_snacks()

    def total_protein(self):
        total = CalorieCount.objects.filter(user=self.user, date=date.today())
        return total.aggregate(Sum('protein'))['protein__sum'] or 0

    def total_fat(self):
        total = CalorieCount.objects.filter(user=self.user, date=date.today())
        return total.aggregate(Sum('fat'))['fat__sum'] or 0

    def total_carbs(self):
        total = CalorieCount.objects.filter(user=self.user, date=date.today())
        return total.aggregate(Sum('carbs'))['carbs__sum'] or 0

    def total_exercise(self):
        total = CalorieCount.objects.filter(user=self.user, date=date.today(), kcals__lt=0)
        if total:
            return -(total.aggregate(Sum('kcals'))['kcals__sum'])
        else:
            return 0

    def net_calories(self):
        return int(self.total_calories()) - int(self.total_exercise())

    def calories_under(self):
        cal = Calculator(self.user)
        return int(cal.target_calories()) - int(self.net_calories())

    def calorie_progress(self):
        cal = Calculator(self.user)
        return int(100-((self.total_calories()/cal.target_calories())*100))

    def exercise_progress(self):
        cal = Calculator(self.user)
        return int((self.total_exercise()/self.user.exercisegoal.target_calories)*100)
