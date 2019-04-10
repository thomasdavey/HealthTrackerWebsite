from django.contrib.auth.forms import PasswordChangeForm
from django.core.checks import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, update_session_auth_hash
from datetime import date
from .forms import MessageForm

from .models import Message
from .models import User


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

    form = MessageForm(request.POST or None)

    if form.is_valid():
        message = form.save(commit=False)
        message.author = request.user
        message.save()
        form = MessageForm()

    context = {
        'messages': messages,
        'selected': 'groups',
        'form': form
    }

    return render(request, 'groups.html', context)


@login_required()
def settings(request):
    accountDetails = [
        {
            'name': request.user.get_full_name(),
            'age': 'myage',
            'weight': 'myweight',
            'height': 'myheight',
            'currentgoals': 'mygoals'
        }
    ]
    healthData = [
        {
            'bmi': 'mybmi',
            'idealweight': 'myideal',
            'targetcals': 'mycals',
            'targetfat': 'myfat',
            'targetcarbs': 'mycarbs',
            'targetprotein': 'myprotein'
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
    context = {
        'details': accountDetails,
        'health' : healthData,
        'foods' : customFoods,
        'exercises' : customExercises,
        'goals' : completedGoals,
        'selected' : 'settings'
    }
    return render(request, 'settings.html', context)
