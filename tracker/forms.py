from django import forms
from .models import Message, Food, Exercise, CalorieCount
from users.models import Profile


class MessageForm(forms.ModelForm):
    message = forms.CharField(widget=forms.TextInput(attrs={'class': 'groups-temp'}))

    class Meta:
        model = Message
        fields = ['message']


class AddFoodForm(forms.ModelForm):

    class Meta:
        model = Food
        fields = ['category', 'name']


class AddCustomFoodForm(forms.ModelForm):

    class Meta:
        model = Food
        fields = ['name', 'calories', 'carbs', 'fat', 'protein']


class AddCustomExerciseForm(forms.ModelForm):

    class Meta:
        model = Exercise
        fields = ['name', 'type', 'calspermin']


class UpdateWeightForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['weight']

