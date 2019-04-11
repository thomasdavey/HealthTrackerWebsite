from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import date
from .forms import MessageForm
from .models import Message


@login_required()
def home(request):
    today = date.today()
    today_format = today.strftime('%A, %d %B %Y')
    return render(request, 'dashboard.html', {'selected': 'Home', 'date': today_format})


@login_required()
def daily_log(request):
    return render(request, 'daily_log.html', {'selected': 'Daily Log'})


@login_required()
def goals(request):
    return render(request, 'goals.html', {'selected': 'Goals'})


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
        'selected': 'Groups',
        'form': form
    }

    return render(request, 'groups.html', context)


@login_required()
def settings(request):
    update_password_form = PasswordChangeForm(user=request.user)
    modal = 'None'
    if request.method == 'POST':
        if 'update_password' in request.POST:
            update_password_form = PasswordChangeForm(data=request.POST, user=request.user)
            modal = 'update_password'
            print('YAY')
            if update_password_form.is_valid():
                update_password_form.save()
                return redirect('tracker-settings')
    context = {
        'selected': 'Settings',
        'update_password_form': update_password_form,
        'modal': modal
    }
    return render(request, 'settings.html', context)

