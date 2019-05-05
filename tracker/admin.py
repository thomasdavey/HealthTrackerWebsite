from django.contrib import admin
from .models import Message
from .models import GroupMember
from .models import Group
from .models import Food
from .models import CalorieCount

admin.site.register(Message)
admin.site.register(GroupMember)
admin.site.register(Group)
admin.site.register(Food)
admin.site.register(CalorieCount)
