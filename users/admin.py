from django.contrib import admin
from .models import Profile
from .models import WeightGoal
from .models import ExerciseGoal

admin.site.register(Profile)
admin.site.register(WeightGoal)
admin.site.register(ExerciseGoal)
