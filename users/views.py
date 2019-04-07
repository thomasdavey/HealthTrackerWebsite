from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from .tokens import account_activation_token


def home(request):
    if request.user.is_authenticated:
        return redirect('tracker-home')
    else:
        return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.sex = form.cleaned_data.get('sex')
            user.profile.height = form.cleaned_data.get('height')
            user.profile.weight = form.cleaned_data.get('weight')
            user.profile.activity_level = form.cleaned_data.get('activity_level')
            user.weightgoal.target_weight = form.cleaned_data.get('target_weight')
            user.weightgoal.target_date = form.cleaned_data.get('target_date')
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Longevity Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            messages.success(request, f'Confirmation email sent. Please check your emails to activate your account!')
            return redirect('users-login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
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
