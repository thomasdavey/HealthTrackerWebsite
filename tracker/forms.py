from django import forms
from .models import Message, Food, Exercise, CalorieCount, Group, GroupMember
from django.contrib.auth.models import User
from users.models import Profile


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

class AddExerciseForm(forms.ModelForm):
    TYPE_CHOICES = [('cardio','Cardio'),('strength','Strength')]

    CARDIO_TEMP = Exercise.objects.raw('SELECT * FROM tracker_exercise WHERE type = "C"')
    CARDIO_CHOICES = []
    for exercise in CARDIO_TEMP:
        CARDIO_CHOICES.append((exercise.id, exercise.name))

    STRENGTH_TEMP = Exercise.objects.raw('SELECT * FROM tracker_exercise WHERE type = "S"')
    STRENGTH_CHOICES = []
    for exercise in STRENGTH_TEMP:
        STRENGTH_CHOICES.append((exercise.id, exercise.name))

    type = forms.ChoiceField(choices=TYPE_CHOICES, widget=forms.Select(attrs={'id': 'type_choice'}))
    cardio = forms.ChoiceField(choices=CARDIO_CHOICES, widget=forms.Select(attrs={'id': 'cardio_choice'}))
    strength = forms.ChoiceField(choices=STRENGTH_CHOICES, widget=forms.Select(attrs={'id': 'strength_choice'}))
    duration = forms.IntegerField(min_value=1)

    class Meta:
        model = Exercise
        fields = ['type','cardio','strength', 'duration']


class AddBreakfastForm(forms.ModelForm):
    CATEGORY_CHOICES = [('meat', 'Meat'),('fruit', 'Fruit'),
                        ('vegetable','Vegetable'),('dairy','Dairy'),
                        ('grain','Grain'),('sweet','Sweet'),
                        ('drink','Drink')]

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

    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select(attrs={'id': 'category_choice_bf'}))
    meat = forms.ChoiceField(choices=MEAT_CHOICES, widget=forms.Select(attrs={'id':'meat_choice_bf'}))
    fruit = forms.ChoiceField(choices=FRUIT_CHOICES, widget=forms.Select(attrs={'id': 'fruit_choice_bf'}))
    vegetable = forms.ChoiceField(choices=VEGETABLE_CHOICES, widget=forms.Select(attrs={'id': 'vegetable_choice_bf'}))
    dairy = forms.ChoiceField(choices=DAIRY_CHOICES, widget=forms.Select(attrs={'id': 'dairy_choice_bf'}))
    grain = forms.ChoiceField(choices=GRAIN_CHOICES, widget=forms.Select(attrs={'id': 'grain_choice_bf'}))
    sweet = forms.ChoiceField(choices=SWEET_CHOICES, widget=forms.Select(attrs={'id': 'sweet_choice_bf'}))
    drink = forms.ChoiceField(choices=DRINK_CHOICES, widget=forms.Select(attrs={'id': 'drink_choice_bf'}))

    class Meta:
        model = CalorieCount
        fields = ['category', 'meat', 'fruit', 'vegetable', 'dairy', 'grain', 'sweet', 'drink']


class AddLunchForm(forms.ModelForm):
    CATEGORY_CHOICES = [('meat', 'Meat'),('fruit', 'Fruit'),
                        ('vegetable','Vegetable'),('dairy','Dairy'),
                        ('grain','Grain'),('sweet','Sweet'),
                        ('drink','Drink')]

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

    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select(attrs={'id': 'category_choice_lu'}))
    meat = forms.ChoiceField(choices=MEAT_CHOICES, widget=forms.Select(attrs={'id':'meat_choice_lu'}))
    fruit = forms.ChoiceField(choices=FRUIT_CHOICES, widget=forms.Select(attrs={'id': 'fruit_choice_lu'}))
    vegetable = forms.ChoiceField(choices=VEGETABLE_CHOICES, widget=forms.Select(attrs={'id': 'vegetable_choice_lu'}))
    dairy = forms.ChoiceField(choices=DAIRY_CHOICES, widget=forms.Select(attrs={'id': 'dairy_choice_lu'}))
    grain = forms.ChoiceField(choices=GRAIN_CHOICES, widget=forms.Select(attrs={'id': 'grain_choice_lu'}))
    sweet = forms.ChoiceField(choices=SWEET_CHOICES, widget=forms.Select(attrs={'id': 'sweet_choice_lu'}))
    drink = forms.ChoiceField(choices=DRINK_CHOICES, widget=forms.Select(attrs={'id': 'drink_choice_lu'}))

    class Meta:
        model = CalorieCount
        fields = ['category', 'meat', 'fruit', 'vegetable', 'dairy', 'grain', 'sweet', 'drink']


class AddDinnerForm(forms.ModelForm):
    CATEGORY_CHOICES = [('meat', 'Meat'),('fruit', 'Fruit'),
                        ('vegetable','Vegetable'),('dairy','Dairy'),
                        ('grain','Grain'),('sweet','Sweet'),
                        ('drink','Drink')]

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

    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select(attrs={'id': 'category_choice_dn'}))
    meat = forms.ChoiceField(choices=MEAT_CHOICES, widget=forms.Select(attrs={'id':'meat_choice_dn'}))
    fruit = forms.ChoiceField(choices=FRUIT_CHOICES, widget=forms.Select(attrs={'id': 'fruit_choice_dn'}))
    vegetable = forms.ChoiceField(choices=VEGETABLE_CHOICES, widget=forms.Select(attrs={'id': 'vegetable_choice_dn'}))
    dairy = forms.ChoiceField(choices=DAIRY_CHOICES, widget=forms.Select(attrs={'id': 'dairy_choice_dn'}))
    grain = forms.ChoiceField(choices=GRAIN_CHOICES, widget=forms.Select(attrs={'id': 'grain_choice_dn'}))
    sweet = forms.ChoiceField(choices=SWEET_CHOICES, widget=forms.Select(attrs={'id': 'sweet_choice_dn'}))
    drink = forms.ChoiceField(choices=DRINK_CHOICES, widget=forms.Select(attrs={'id': 'drink_choice_dn'}))

    class Meta:
        model = CalorieCount
        fields = ['category', 'meat', 'fruit', 'vegetable', 'dairy', 'grain', 'sweet', 'drink']


class AddSnackForm(forms.ModelForm):
    CATEGORY_CHOICES = [('meat', 'Meat'),('fruit', 'Fruit'),
                        ('vegetable','Vegetable'),('dairy','Dairy'),
                        ('grain','Grain'),('sweet','Sweet'),
                        ('drink','Drink')]

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

    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select(attrs={'id': 'category_choice_sk'}))
    meat = forms.ChoiceField(choices=MEAT_CHOICES, widget=forms.Select(attrs={'id':'meat_choice_sk'}))
    fruit = forms.ChoiceField(choices=FRUIT_CHOICES, widget=forms.Select(attrs={'id': 'fruit_choice_sk'}))
    vegetable = forms.ChoiceField(choices=VEGETABLE_CHOICES, widget=forms.Select(attrs={'id': 'vegetable_choice_sk'}))
    dairy = forms.ChoiceField(choices=DAIRY_CHOICES, widget=forms.Select(attrs={'id': 'dairy_choice_sk'}))
    grain = forms.ChoiceField(choices=GRAIN_CHOICES, widget=forms.Select(attrs={'id': 'grain_choice_sk'}))
    sweet = forms.ChoiceField(choices=SWEET_CHOICES, widget=forms.Select(attrs={'id': 'sweet_choice_sk'}))
    drink = forms.ChoiceField(choices=DRINK_CHOICES, widget=forms.Select(attrs={'id': 'drink_choice_sk'}))

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

