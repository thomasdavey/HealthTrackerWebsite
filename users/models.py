from django.db import models
from django.contrib.auth.models import User
from decimal import *


class Profile(models.Model):
    SEX_CHOICES = [('M', 'Male'), ('F', 'Female')]
    ACTIVITY_LEVEL_CHOICES = [('1.2', 'Less than 2 hours per week'), ('1.375', '2-5 hours per week'),
                              ('1.55', '6-10 hours per week'), ('1.725', 'More than 10 hours per week')]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, null=True)
    height = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)
    activity_level = models.CharField(max_length=5, choices=ACTIVITY_LEVEL_CHOICES, null=True)

    def __str__(self):
        return f'{self.user.username}'


class WeightGoal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    target_weight = models.IntegerField(null=True)
    target_date = models.DateField(null=True)

    def __str__(self):
        return f'{self.user.username}'
