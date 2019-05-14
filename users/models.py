from django.db import models
from django.contrib.auth.models import User
from decimal import *
from tracker import calculator
from datetime import date


# Model containing profile information for a registered user
class Profile(models.Model):
    SEX_CHOICES = [('M', 'Male'), ('F', 'Female')]
    ACTIVITY_LEVEL_CHOICES = [('1.2', 'Sedentary'), ('1.375', 'Lightly Active'),
                              ('1.55', 'Moderately Active'), ('1.725', 'Highly Active')]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, null=True)
    height = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)
    activity_level = models.CharField(max_length=5, choices=ACTIVITY_LEVEL_CHOICES, null=True)
    image = models.ImageField(default='default.png', upload_to='profile-pics')

    def __str__(self):
        return f'{self.user.username}'


# Model containing information on weight goal objects
class WeightGoal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    start_weight = models.IntegerField(null=True)
    target_weight = models.IntegerField(null=True)
    start_date = models.DateField(auto_now_add=True, null=True)
    target_date = models.DateField(null=True)

    def __str__(self):
        return f'{self.user.username}'


# Model containing information on exercise goal objects
class ExerciseGoal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    target_calories = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.user.username}'

