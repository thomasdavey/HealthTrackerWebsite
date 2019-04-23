from django import forms
from .models import Message, Food, Exercise, CalorieCount
from users.models import Profile


class MessageForm(forms.ModelForm):
    message = forms.CharField(widget=forms.TextInput(attrs={'class': 'groups-temp'}))

    class Meta:
        model = Message
        fields = ['message']


class AddFoodForm(forms.ModelForm):
    CATEGORY_CHOICES = [(0, 'Meat'),(1, 'Fruit'),(2,'Vegetable'),(3,'Dairy'),(4,'Grain'),(5,'Sweet'),(6,'Drink')]

    MEAT_TEMP = Food.objects.raw('SELECT * FROM tracker_food WHERE category = "Meat"')
    MEAT_CHOICES = []
    for food in MEAT_TEMP:
        MEAT_CHOICES.append((food.id, food.name))

    FRUIT_TEMP = Food.objects.raw('SELECT * FROM tracker_food WHERE category = "Fruit"')
    FRUIT_CHOICES = []
    for food in FRUIT_TEMP:
        FRUIT_CHOICES.append((food.id, food.name))

    VEGETABLE_TEMP = Food.objects.raw('SELECT * FROM tracker_food WHERE category = "Vegetable"')
    VEGETABLE_CHOICES = []
    for food in VEGETABLE_TEMP:
        VEGETABLE_CHOICES.append((food.id, food.name))

    DAIRY_TEMP = Food.objects.raw('SELECT * FROM tracker_food WHERE category = "Dairy"')
    DAIRY_CHOICES = []
    for food in DAIRY_TEMP:
        DAIRY_CHOICES.append((food.id, food.name))

    GRAIN_TEMP = Food.objects.raw('SELECT * FROM tracker_food WHERE category = "Grain"')
    GRAIN_CHOICES = []
    for food in GRAIN_TEMP:
        GRAIN_CHOICES.append((food.id, food.name))

    SWEET_TEMP = Food.objects.raw('SELECT * FROM tracker_food WHERE category = "Sweet"')
    SWEET_CHOICES = []
    for food in SWEET_TEMP:
        SWEET_CHOICES.append((food.id, food.name))

    DRINK_TEMP = Food.objects.raw('SELECT * FROM tracker_food WHERE category = "Drink"')
    DRINK_CHOICES = []
    for food in DRINK_TEMP:
        DRINK_CHOICES.append((food.id, food.name))

    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select(attrs={'id': 'category_choice'}))
    meat = forms.ChoiceField(choices=MEAT_CHOICES, widget=forms.Select(attrs={'id':'meat_choice'}))
    fruit = forms.ChoiceField(choices=FRUIT_CHOICES, widget=forms.Select(attrs={'id': 'fruit_choice'}))
    vegetable = forms.ChoiceField(choices=VEGETABLE_CHOICES, widget=forms.Select(attrs={'id': 'vegetable_choice'}))
    dairy = forms.ChoiceField(choices=DAIRY_CHOICES, widget=forms.Select(attrs={'id': 'dairy_choice'}))
    grain = forms.ChoiceField(choices=GRAIN_CHOICES, widget=forms.Select(attrs={'id': 'grain_choice'}))
    sweet = forms.ChoiceField(choices=SWEET_CHOICES, widget=forms.Select(attrs={'id': 'sweet_choice'}))
    drink = forms.ChoiceField(choices=DRINK_CHOICES, widget=forms.Select(attrs={'id': 'drink_choice'}))

    class Meta:
        model = CalorieCount
        fields = ['category', 'meat', 'fruit', 'vegetable', 'dairy', 'grain', 'sweet', 'drink']


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

