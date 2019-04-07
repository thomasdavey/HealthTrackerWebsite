from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from datetime import date


class UserRegisterForm(UserCreationForm):
    SEX_CHOICES = [('M','Male'),('F','Female')]
    ACTIVITY_LEVEL_CHOICES = [(1.2,'Less than 2 hours per week'),(1.375,'2-5 hours per week'),
                              (1.55,'6-10 hours per week'),(1.725,'More than 10 hours per week')]

    email = forms.EmailField
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    birth_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'placeholder': 'dd/mm/yyyy', 'type': 'date'}))
    sex = forms.ChoiceField(required=True, choices=SEX_CHOICES)
    height = forms.IntegerField(required=True)
    weight = forms.IntegerField(required=True)
    activity_level = forms.ChoiceField(required=True, choices=ACTIVITY_LEVEL_CHOICES)
    target_weight = forms.IntegerField(required=True)
    target_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'placeholder': 'dd/mm/yyyy', 'type': 'date'}))

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        verify_age = date.today()
        verify_age = verify_age.replace(year=verify_age.year-16)

        print(birth_date)
        print(verify_age)

        if birth_date > date.today():
            raise forms.ValidationError("Enter a valid date.")
        elif birth_date > verify_age:
            raise forms.ValidationError("You must be at least 16 years old to use Longevity.")

        return birth_date

    def clean_target_date(self):
        target_date = self.cleaned_data['target_date']

        print(target_date)
        print(date.today())

        if target_date <= date.today():
            raise forms.ValidationError("Enter a valid date.")
        return target_date

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'birth_date', 'sex',
                  'height', 'weight', 'activity_level', 'target_weight', 'target_date']
