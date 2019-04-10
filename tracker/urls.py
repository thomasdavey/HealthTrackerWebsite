from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='tracker-home'),
    path('log/', views.daily_log, name='tracker-daily-log'),
    path('goals/', views.goals, name='tracker-goals'),
    path('groups/', views.groups, name='tracker-groups'),
    path('settings/', views.settings, name='tracker-settings'),
]
