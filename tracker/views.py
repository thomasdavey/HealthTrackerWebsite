from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.db.models import Sum, F
from datetime import date
from users.forms import AccountUpdateForm, ProfileUpdateForm
from .forms import MessageForm, AddCustomFoodForm, AddFoodForm, UpdateWeightForm, AddCustomExerciseForm
from .models import Message, Food, Exercise
from .models import GroupMember
from .models import Group, CalorieCount
from tracker import calculator
from users.models import WeightGoal

@login_required()
def home(request):
    today = date.today()
    today_format = today.strftime('%A, %d %B %Y')
    return render(request, 'dashboard.html', {'selected': 'Home', 'date': today_format})


@login_required()
def daily_log(request):
    user = request.user

    age = date.today().year - user.profile.birth_date.year - \
        ((date.today().month, date.today().day) < (user.profile.birth_date.month, user.profile.birth_date.day))
    meta_rate = calculator.metabolic_rate(int(user.profile.weight), int(user.profile.height), int(age))
    extremity = calculator.get_weight_loss_extremity(user)
    daily_cals = calculator.daily_cal(meta_rate, user.profile.activity_level)
    target_cals = calculator.target_calories(meta_rate, user.profile.activity_level, extremity)

    target_bk = int(calculator.target_breakfast(target_cals))
    target_l = int(calculator.target_lunch(target_cals))
    target_dn = int(calculator.target_dinner(target_cals))
    target_sn = int(calculator.target_snacks(target_cals))

    target_protein = int(calculator.target_protein(user.profile.weight))
    target_fat = int(calculator.target_fat(daily_cals))
    target_carbs = int(calculator.target_carbs(daily_cals, target_fat, target_protein))

    food_form = AddFoodForm(request.POST or None)

    form = AddCustomFoodForm(request.POST or None)
    if form.is_valid():
        food = form.save(commit=False)
        food.user = request.user
        food.category = "Custom"
        food.save()

    weight_form = UpdateWeightForm(data=request.POST, instance=request.user.profile)
    if weight_form.is_valid():
        weight_form.save()

    exercise_form = AddCustomExerciseForm(request.POST or None)
    if exercise_form.is_valid():
        exercise = exercise_form.save(commit=False)
        exercise.user = request.user
        exercise.save()

    breakfast = CalorieCount.objects.filter(user=user, date=date.today(), meal='BF')
    bcals = breakfast.aggregate(Sum('kcals'))['kcals__sum'] or 0
    lunch = CalorieCount.objects.filter(user=user, date=date.today(), meal='LU')
    lcals = lunch.aggregate(Sum('kcals'))['kcals__sum'] or 0
    dinner = CalorieCount.objects.filter(user=user, date=date.today(), meal='DN')
    dcals = dinner.aggregate(Sum('kcals'))['kcals__sum'] or 0
    snacks = CalorieCount.objects.filter(user=user, date=date.today(), meal='SK')
    scals = snacks.aggregate(Sum('kcals'))['kcals__sum'] or 0
    total_calories = bcals + lcals + dcals + scals

    total_p = CalorieCount.objects.filter(user=user, date=date.today())
    totalp = total_p.aggregate(Sum('protein'))['protein__sum'] or 0
    total_f = CalorieCount.objects.filter(user=user, date=date.today())
    totalf = total_f.aggregate(Sum('fat'))['fat__sum'] or 0
    total_c = CalorieCount.objects.filter(user=user, date=date.today())
    totalc = total_c.aggregate(Sum('carbs'))['carbs__sum'] or 0

    # CHANGE THIS TO ACCESS USERS EXERCISE CALORIES BURNED
    exercise_cals = 0
    net_calories = calculator.net_calories(total_calories, exercise_cals)
    cals_under = calculator.cals_under_budget(target_cals, net_calories)

    context = {
        'selected': 'Daily Log',
        'form': form,
        'foodForm': food_form,
        'target_cals': target_cals,
        'breakfast': bcals,
        'lunch': lcals,
        'dinner': dcals,
        'snacks': scals,
        'targetb': target_bk,
        'targetl': target_l,
        'targetd': target_dn,
        'targets': target_sn,
        'targetc': target_carbs,
        'targetf': target_fat,
        'targetp': target_protein,
        'totalp': totalp,
        'totalf': totalf,
        'totalc': totalc,
        'cals_under': cals_under,
        'net_cals': net_calories,
        'ex_cals': exercise_cals,
        'weightForm': weight_form,
        'exerciseForm': exercise_form
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

