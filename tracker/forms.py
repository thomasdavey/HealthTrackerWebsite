from django import forms
from .models import Message, Food, Exercise, CalorieCount
from users.models import Profile


class MessageForm(forms.ModelForm):
    message = forms.CharField(widget=forms.TextInput(attrs={'class': 'groups-temp'}))

    class Meta:
        model = Message
        fields = ['message']

class AddExerciseForm(forms.ModelForm):
    TYPE_CHOICES = [(0,'Cardio'),(1,'Strength')]

    CARDIO_TEMP = Exercise.objects.raw('SELECT * FROM tracker_exercise WHERE type = "C"')
    CARDIO_CHOICES = []
    for exercise in CARDIO_TEMP:
        CARDIO_CHOICES.append((exercise.id, exercise.name))

    STRENGTH_TEMP = Exercise.objects.raw('SELECT * FROM tracker_exercise WHERE type = "S"')
    STRENGTH_CHOICES = []
    for exercise in STRENGTH_TEMP:
        STRENGTH_CHOICES.append((exercise.id, exercise.name))

    type = forms.ChoiceField(choices=TYPE_CHOICES, widget=forms.Select(attrs={'id': 'type-choice'}))
    cardio = forms.ChoiceField(choices=CARDIO_CHOICES, widget=forms.Select(attrs={'id': 'cardio-choice'}))
    strength = forms.ChoiceField(choices=STRENGTH_CHOICES, widget=forms.Select(attrs={'id': 'strength-choice'}))

    class Meta:
        model = Exercise
        fields = ['type','cardio','strength']

class AddFoodForm(forms.ModelForm):

    class Meta:
        model = Food
        fields = ['category', 'name']


class AddCustomFoodForm(forms.ModelForm):

    class Meta:
        model = Food
        fields = ['name', 'category', 'calories', 'carbs', 'fat', 'protein']


class AddCustomExerciseForm(forms.ModelForm):

    class Meta:
        model = Exercise
        fields = ['name', 'type', 'calspermin']


class UpdateWeightForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['weight']

