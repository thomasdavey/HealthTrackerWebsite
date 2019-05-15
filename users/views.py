from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from datetime import date
from dateutil.relativedelta import *
from tracker.calculator import Calculator
from .forms import UserRegisterForm
from .forms import ProfileRegistrationForm
from .forms import GoalRegistrationForm
from .tokens import account_activation_token


# Method for redirecting a user to the home page template
def home(request):
    if request.user.is_authenticated:
        return redirect('tracker-home')
    else:
        return render(request, 'home.html')


# Method for passing the correct information to the register page template
def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileRegistrationForm(request.POST)
        goal_form = GoalRegistrationForm(request.POST)

        # this generates the registration form and saves a default exercise goal for the user
        if user_form.is_valid() and profile_form.is_valid() and goal_form.is_valid():
            user = user_form.save()
            user.profile.birth_date = profile_form.cleaned_data.get('birth_date')
            user.profile.sex = profile_form.cleaned_data.get('sex')
            user.profile.height = profile_form.cleaned_data.get('height')
            user.profile.weight = profile_form.cleaned_data.get('weight')
            user.profile.activity_level = profile_form.cleaned_data.get('activity_level')
            user.weightgoal.start_weight = profile_form.cleaned_data.get('weight')
            user.weightgoal.target_weight = goal_form.cleaned_data.get('target_weight')
            user.weightgoal.target_date = goal_form.cleaned_data.get('target_date')
            cal = Calculator(user)
            user.exercisegoal.target_calories = int(cal.target_calories() * ((float(user.profile.activity_level) - 1)/2))
            now = date.today()
            user.exercisegoal.review_date = now + relativedelta(months=+1)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Longevity Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            messages.success(request, f'Confirmation email sent. Please check your emails to activate your account!')
            return redirect('users-login')
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileRegistrationForm()
        goal_form = GoalRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form, 'goal_form': goal_form})


# Method for passing the correct information to the account activation page template
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, f'Your account was successfully activated! You can now sign in below.')
        return redirect('users-login')
    else:
        messages.error(request, f'An error occurred. Your account was not activated.')
        return redirect('users-login')

