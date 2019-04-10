from django.db import models
from django.contrib.auth.models import User


# Create your models here.
from SE2 import settings


class Message(models.Model):
    group_id = models.CharField(max_length=100, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, db_column='author')
    message = models.TextField(null=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


class GroupMember(models.Model):
    group_id = models.CharField(max_length=100, null=True)
    member = models.ForeignKey(User, on_delete=models.CASCADE, db_column='member')
