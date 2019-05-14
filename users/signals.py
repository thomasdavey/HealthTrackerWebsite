from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from .models import WeightGoal
from .models import ExerciseGoal


# This file contains methods for creating and saving profiles, weight goals, and exercise goals.
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=User)
def create_weight_goal(sender, instance, created, **kwargs):
    if created:
        WeightGoal.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_weight_goal(sender, instance, **kwargs):
    instance.weightgoal.save()


@receiver(post_save, sender=User)
def create_exercise_goal(sender, instance, created, **kwargs):
    if created:
        ExerciseGoal.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_exercise_goal(sender, instance, **kwargs):
    instance.exercisegoal.save()
