from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.db.models import Sum, F
from datetime import date, timedelta, datetime
from users.forms import AccountUpdateForm, ProfileUpdateForm
from .forms import AddFoodForm
from .forms import MessageForm, AddCustomFoodForm, UpdateWeightForm, AddCustomExerciseForm, AddCardioForm, AddStrengthForm, CreateGroupForm, CreateGroupMemberForm
from .models import Message, Food, Exercise
from .models import GroupMember
from .models import Group, CalorieCount
from .calculator import Calculator, Accessor


@login_required()
def home(request):
    today = date.today()
    today_format = today.strftime('%A, %d %B %Y')

    context = {
        'selected': 'Home',
        'date': today_format
    }

    return render(request, 'dashboard.html', context)


@login_required()
def daily_log(request):
    user = request.user
    cal = Calculator(user)
    acc = Accessor(user)

    food_form = AddFoodForm()
    if request.method == 'POST':
        if 'Breakfast' in request.POST:
            item = request.POST[request.POST['category']]
            query = Food.objects.filter(id=item)
            for item in query:
                my_food = CalorieCount(user=request.user, kcals=item.calories, meal='BF',
                                       fat=item.fat, carbs=item.carbs, protein=item.protein)
                my_food.save()

        if 'Lunch' in request.POST:
            item = request.POST[request.POST['category']]
            query = Food.objects.filter(id=item)
            for item in query:
                my_food = CalorieCount(user=request.user, kcals=item.calories, meal='LU',
                                       fat=item.fat, carbs=item.carbs, protein=item.protein)
                my_food.save()
        if 'Dinner' in request.POST:
            item = request.POST[request.POST['category']]
            query = Food.objects.filter(id=item)
            for item in query:
                my_food = CalorieCount(user=request.user, kcals=item.calories, meal='DN',
                                       fat=item.fat, carbs=item.carbs, protein=item.protein)
                my_food.save()
        if 'Snack' in request.POST:
            item = request.POST[request.POST['category']]
            query = Food.objects.filter(id=item)
            for item in query:
                my_food = CalorieCount(user=request.user, kcals=item.calories, meal='SK',
                                       fat=item.fat, carbs=item.carbs, protein=item.protein)
                my_food.save()

    strength_form = AddStrengthForm()
    cardio_form = AddCardioForm()
    if request.method == 'POST':
        if 'strength' in request.POST or 'cardio' in request.POST:
            weight_lbs = int(user.profile.weight * 2.20462)
            duration = int(request.POST.get('duration', 0))
            item = request.POST['exercise']
            query = Exercise.objects.filter(id=item)
            for item in query:
                calories = int(item.calspermin * duration * weight_lbs)
                CalorieCount.objects.create(user=request.user, kcals=-calories)

    custom_food_form = AddCustomFoodForm(request.POST or None)
    if custom_food_form.is_valid():
        food = custom_food_form.save(commit=False)
        food.user = request.user
        food.save()

    custom_exercise_form = AddCustomExerciseForm(request.POST or None)
    if custom_exercise_form.is_valid():
        exercise = custom_exercise_form.save(commit=False)
        exercise.user = request.user
        exercise.save()

    update_weight_form = UpdateWeightForm(instance=request.user.profile)
    if 'update_weight' in request.POST:
        update_weight_form = UpdateWeightForm(data=request.POST, instance=request.user.profile)
        if update_weight_form.is_valid():
            update_weight_form.save()
            return redirect('tracker-daily-log')

    context = {
        'selected': 'Daily Log',
        'cal': cal,
        'acc': acc,
        'food_form': food_form,
        'custom_food_form': custom_food_form,
        'strength_form': strength_form,
        'cardio_form': cardio_form,
        'custom_exercise_form': custom_exercise_form,
        'update_weight_form': update_weight_form,
    }

    return render(request, 'daily_log.html', context)


@login_required()
def goals(request):
    user = request.user
    cal = Calculator(user)

    days = []
    calories = []
    for n in range(7):
        day = date.today() - timedelta(days=7-n)
        count = CalorieCount.objects.filter(user=user, date=day)
        calories.append(count.aggregate(Sum('kcals'))['kcals__sum'] or 0)
        days.append(day.strftime('%d %b'))

    print(calories)

    context = {
        'selected': 'Goals',
        'cal': cal,
        'days': days,
        'calories': calories,
    }
    return render(request, 'goals.html', context)


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

    form = MessageForm()
    create_group_form = CreateGroupForm()
    create_group_member_form = CreateGroupMemberForm()

    if request.method == 'POST':
        print(request.POST)
        if 'message' in request.POST:
            form = MessageForm(data=request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.author = request.user
                message.group = Group.objects.get(id=request.POST.get('group'))
                message.save()
        elif 'create' in request.POST:
            create_group_form = CreateGroupForm(data=request.POST)
            if create_group_form.is_valid():
                group = create_group_form.save(commit=False)
                group.creator = request.user
                group.save()
                GroupMember.objects.create(group=group, user=request.user)
                query = User.objects.filter(username='longevity')
                longevity = query[0]
                welcome = "Welcome to your new group! Add some friends to start discussing your goals!"
                Message.objects.create(group=group, author=longevity, message=welcome)
                return redirect('tracker-groups')
        elif 'add' in request.POST:
            create_group_member_form = CreateGroupMemberForm(data=request.POST)
            if create_group_member_form.is_valid():
                group = Group.objects.get(id=request.POST.get('add'))
                user = User.objects.get(username=request.POST.get('username'))
                GroupMember.objects.create(group=group, user=user)
                query = User.objects.filter(username='admin')
                admin = query[0]
                message = user.first_name + " " + user.last_name + " was added to the group."
                Message.objects.create(group=group, author=admin, message=message)
                return redirect('tracker-groups')

    context = {
        'groups': groups,
        'messages': messages,
        'last': last,
        'selected': 'Groups',
        'form': form,
        'create_group_form': create_group_form,
        'create_group_member_form': create_group_member_form
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

    my_exercises = Exercise.objects.filter(user=request.user)
    exercises = list(my_exercises.values('name'))

    context = {
        'selected': 'Settings',
        'format_date': format_date,
        'update_account_form': update_account_form,
        'update_password_form': update_password_form,
        'update_profile_form': update_profile_form,
        'modal': modal,
        'exercises': exercises
    }
    return render(request, 'settings.html', context)

