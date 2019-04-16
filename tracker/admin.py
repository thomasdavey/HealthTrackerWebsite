from django.contrib import admin
from .models import Message
from .models import GroupMember
from .models import Group

admin.site.register(Message)
admin.site.register(GroupMember)
admin.site.register(Group)
