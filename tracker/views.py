from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date


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
    return render(request, 'groups.html', {'selected': 'groups'})


@login_required()
def settings(request):
    return render(request, 'settings.html', {'selected': 'settings'})
