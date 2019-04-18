from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from datetime import date
from users.forms import AccountUpdateForm ,ProfileUpdateForm
from .forms import MessageForm, AddCustomFoodForm, AddFoodForm
from .models import Message, Food
from .models import GroupMember
from .models import Group


@login_required()
def home(request):
    today = date.today()
    today_format = today.strftime('%A, %d %B %Y')
    return render(request, 'dashboard.html', {'selected': 'Home', 'date': today_format})


@login_required()
def daily_log(request):
    form = AddCustomFoodForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()

    foods = Food.objects.all()

    context = {
        'selected': 'Daily Log',
        'foods': foods
    }

    return render(request, 'daily_log.html', context)


@login_required()
def goals(request):
    return render(request, 'goals.html', {'selected': 'Goals'})


@login_required()
def groups(request):
    user = request.user
    groups = GroupMember.objects.raw('SELECT * FROM tracker_groupmember WHERE user_id = ' + str(user.id))
    messages = []
    last = []

    for item in groups:
        messages.append(Message.objects.raw('SELECT * FROM tracker_message WHERE group_id = ' + str(item.group.id)))

    def sortDate(elem):
        return elem[-1].posted

    messages.sort(key=sortDate, reverse=True)

    for set in messages:
        last.append(set[-1])

    form = MessageForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = Group.objects.get(id=request.POST.get('group'))
            message.save()
            form = MessageForm()

    context = {
        'groups': groups,
        'messages': messages,
        'last': last,
        'selected': 'Groups',
        'form': form
    }

    return render(request, 'groups.html', context)


@login_required()
def settings(request):
    joined_date = request.user.date_joined
    format_date = joined_date.strftime('%d/%m/%Y')
    update_account_form = AccountUpdateForm(instance=request.user)
    update_password_form = PasswordChangeForm(user=request.user)
    update_profile_form = ProfileUpdateForm(instance=request.user.profile)
    modal = 'none'
    if request.method == 'POST':
        if 'update_account' in request.POST:
            print(request.POST)
            update_account_form = AccountUpdateForm(data=request.POST, instance=request.user)
            modal = 'update_account'
            if update_account_form.is_valid():
                update_account_form.save()
                messages.success(request, f'Account details successfully updated!')
                return redirect('tracker-settings')
        if 'update_password' in request.POST:
            update_password_form = PasswordChangeForm(data=request.POST, user=request.user)
            modal = 'update_password'
            if update_password_form.is_valid():
                update_password_form.save()
                update_session_auth_hash(request, update_password_form.user)
                messages.success(request, f'Password successfully changed!')
                return redirect('tracker-settings')
        if 'update_profile' in request.POST:
            update_profile_form = ProfileUpdateForm(data=request.POST, files=request.FILES, instance=request.user.profile)
            print(request.FILES)
            modal = 'update_profile'
            if update_profile_form.is_valid():
                update_profile_form.save()
                messages.success(request, f'Profile successfully updated!')
                return redirect('tracker-settings')
    context = {
        'selected': 'Settings',
        'format_date': format_date,
        'update_account_form': update_account_form,
        'update_password_form': update_password_form,
        'update_profile_form': update_profile_form,
        'modal': modal
    }
    return render(request, 'settings.html', context)

