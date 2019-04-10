from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date

from .models import Message
accountDetails = [
    {
        'name': 'myname',
        'age' : 'myage',
        'weight' : 'myweight',
        'height' : 'myheight',
        'currentgoals' : 'mygoals'
    }
]

healthData = [
    {
        'bmi': 'mybmi',
        'idealweight' : 'myideal',
        'targetcals': 'mycals',
        'targetfat': 'myfat',
        'targetcarbs' : 'mycarbs',
        'targetprotein' : 'myprotein'
    }
]

customFoods = [
    {
        'food': 'foodname'
    }
]

customExercises = [
    {
        'exercise': 'exercisename'
    }
]

completedGoals = [
    {
        'goal': 'mygoal'
    }
]

@login_required()
def home(request):
    today = date.today()
    today_format = today.strftime('%A, %d %B %Y')
    return render(request, 'dashboard.html', {'selected': 'home', 'date': today_format})


@login_required()
def daily_log(request):
    return render(request, 'daily_log.html', {'selected': 'daily_log'})


@login_required()
def goals(request):
    return render(request, 'goals.html', {'selected': 'goals'})


@login_required()
def groups(request):
    messages = Message.objects.all()
    context = {
        'messages': messages,
        'selected': 'groups'
    }
    return render(request, 'groups.html', context)


@login_required()
def settings(request):
    context = {
        'details': accountDetails,
        'health' : healthData,
        'foods' : customFoods,
        'exercises' : customExercises,
        'goals' : completedGoals
    }
    return render(request, 'settings.html', context, {'selected': 'settings'})
