from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Message(models.Model):
    group_id = models.CharField(max_length=100, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    message = models.TextField(null=True)
    date_posted = models.DateTimeField(auto_now_add=True)


class GroupMember(models.Model):
    group_id = models.CharField(max_length=100, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
