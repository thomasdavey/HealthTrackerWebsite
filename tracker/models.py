from django.db import models
from django.contrib.auth.models import User


# Create your models here.
from SE2 import settings


class Group(models.Model):
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'Group {self.id}: {self.name}'


class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'Group {self.group.id} member: {self.user.username}'


class Message(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.TextField(null=True)
    posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Group {self.group.id}: {self.author.username} - {self.message}'


class Food(models.Model):

    CATEGORIES = (
        ('Meat', 'Meat'),
        ('Fruit', 'Fruit'),
        ('Vegetable', 'Vegetable'),
        ('Dairy', 'Dairy'),
        ('Grain', 'Grain'),
        ('Sweet', 'Sweet'),
        ('Drink', 'Drink')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, null=True)
    calories = models.IntegerField(null=True)
    carbs = models.IntegerField(null=True)
    fat = models.IntegerField(null=True)
    protein = models.IntegerField(null=True)
    category = models.CharField(max_length=20, choices=CATEGORIES, null=True)

    def __str__(self):
        return f'Food {self.name}'


class Exercise(models.Model):
    TYPE = (
        ('C', 'Cardio'),
        ('S', 'Strength')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, null=True)
    type = models.CharField(max_length=20, choices=TYPE, null=True)
    calspermin = models.IntegerField(null=True)

    def __str__(self):
        return f'Exercise {self.name}'


class CalorieCount(models.Model):
    MEALS = (
        ('BF', 'Breakfast'),
        ('LU', 'Lunch'),
        ('DN', 'Dinner'),
        ('SK', 'Snacks'),
        ('EX', 'Exercise')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True)
    kcals = models.IntegerField(null=True)
    fat = models.IntegerField(null=True)
    carbs = models.IntegerField(null=True)
    protein = models.IntegerField(null=True)
    meal = models.CharField(max_length=20, choices=MEALS, null=True)

    def __str__(self):
        return f'CalorieCount {self.kcals}'
