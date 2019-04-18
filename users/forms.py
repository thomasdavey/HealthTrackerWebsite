from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from datetime import date
from .models import Profile
from .models import WeightGoal


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class ProfileRegistrationForm(forms.ModelForm):
    birth_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'placeholder': 'dd/mm/yyyy', 'type': 'date'}))

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        verify_age = date.today()
        verify_age = verify_age.replace(year=verify_age.year-16)

        if birth_date > date.today():
            raise forms.ValidationError("Enter a valid date.")
        elif birth_date > verify_age:
            raise forms.ValidationError("You must be at least 16 years old to use Longevity.")

        return birth_date

    class Meta:
        model = Profile
        fields = ['birth_date', 'sex', 'height', 'weight', 'activity_level']


class GoalRegistrationForm(forms.ModelForm):
    target_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'placeholder': 'dd/mm/yyyy', 'type': 'date'}))

    def clean_target_date(self):
        target_date = self.cleaned_data['target_date']

        if target_date <= date.today():
            raise forms.ValidationError("Enter a valid date.")
        return target_date

    class Meta:
        model = WeightGoal
        fields = ['target_weight', 'target_date']


class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    image = forms.FileField(required=False, widget=forms.FileInput)

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        verify_age = date.today()
        verify_age = verify_age.replace(year=verify_age.year-16)

        if birth_date > date.today():
            raise forms.ValidationError("Enter a valid date.")
        elif birth_date > verify_age:
            raise forms.ValidationError("You must be at least 16 years old to use Longevity.")

        return birth_date

    class Meta:
        model = Profile
        fields = ['birth_date', 'sex', 'height', 'weight', 'activity_level', 'image']


class WeightGoalUpdateForm(forms.ModelForm):

    def clean_target_date(self):
        target_date = self.cleaned_data['target_date']

        if target_date <= date.today():
            raise forms.ValidationError("Enter a valid date.")
        return target_date

    class Meta:
        model = WeightGoal
        fields = ['target_weight', 'target_date']


