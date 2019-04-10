from django.contrib import admin
from .models import Message
from .models import GroupMember

admin.site.register(Message)
admin.site.register(GroupMember)