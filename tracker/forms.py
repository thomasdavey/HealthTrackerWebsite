from django import forms
from .models import Message, Food, Exercise, CalorieCount, Group, GroupMember
from django.contrib.auth.models import User
from users.models import Profile, WeightGoal, ExerciseGoal


class MessageForm(forms.ModelForm):
    message = forms.CharField(widget=forms.TextInput(attrs={'class': 'groups-temp'}))

    class Meta:
        model = Message
        fields = ['message']


class CreateGroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ['name']


class CreateGroupMemberForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(), required=True)

    def clean_username(self):
        username = self.cleaned_data['username']
        query = User.objects.filter(username=username)

        if not query:
            raise forms.ValidationError("User not found.")

        return username

    class Meta:
        model = GroupMember
        fields = ['username']


class AddStrengthForm(forms.ModelForm):

    STRENGTH_TEMP = Exercise.objects.raw('SELECT * FROM tracker_exercise WHERE type = "S"')
    STRENGTH_CHOICES = []
    for exercise in STRENGTH_TEMP:
        STRENGTH_CHOICES.append((exercise.id, exercise.name))

    exercise = forms.ChoiceField(choices=STRENGTH_CHOICES, widget=forms.Select())
    duration = forms.IntegerField(min_value=1)

    class Meta:
        model = Exercise
        fields = ['exercise', 'duration']


class AddCardioForm(forms.ModelForm):

    CARDIO_TEMP = Exercise.objects.raw('SELECT * FROM tracker_exercise WHERE type = "C"')
    CARDIO_CHOICES = []
    for exercise in CARDIO_TEMP:
        CARDIO_CHOICES.append((exercise.id, exercise.name))

    exercise = forms.ChoiceField(choices=CARDIO_CHOICES, widget=forms.Select())
    duration = forms.IntegerField(min_value=1)

    class Meta:
        model = Exercise
        fields = ['exercise', 'duration']


class AddFoodForm(forms.ModelForm):
    CATEGORY_CHOICES = [('meat', 'Meat'),('fruit', 'Fruit'),
                        ('vegetable','Vegetable'),('dairy','Dairy'),
                        ('grain','Grain'),('sweet','Sweet'),
                        ('drink','Drink'),('custom','Custom')]

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

    CUSTOM_TEMP = Food.objects.raw('SELECT * FROM tracker_food WHERE category = "Custom"')
    CUSTOM_CHOICES = []
    for food in CUSTOM_TEMP:
        CUSTOM_CHOICES.append((food.id, food.name))

    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select())
    meat = forms.ChoiceField(choices=MEAT_CHOICES, widget=forms.Select())
    fruit = forms.ChoiceField(choices=FRUIT_CHOICES, widget=forms.Select())
    vegetable = forms.ChoiceField(choices=VEGETABLE_CHOICES, widget=forms.Select())
    dairy = forms.ChoiceField(choices=DAIRY_CHOICES, widget=forms.Select())
    grain = forms.ChoiceField(choices=GRAIN_CHOICES, widget=forms.Select())
    sweet = forms.ChoiceField(choices=SWEET_CHOICES, widget=forms.Select())
    drink = forms.ChoiceField(choices=DRINK_CHOICES, widget=forms.Select())
    custom = forms.ChoiceField(choices=CUSTOM_CHOICES, widget=forms.Select())

    class Meta:
        model = CalorieCount
        fields = ['category', 'meat', 'fruit', 'vegetable', 'dairy', 'grain', 'sweet', 'drink', 'custom']


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


class UpdateWeightGoalForm(forms.ModelForm):

    class Meta:
        model = WeightGoal
        fields = ['target_weight', 'target_date']


class UpdateExerciseGoalForm(forms.ModelForm):

    class Meta:
        model = ExerciseGoal
        fields = ['target_calories']
