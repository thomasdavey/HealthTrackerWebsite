from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='users-home'),
    path('register/', views.register, name='users-register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='users-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='login.html'), name='users-logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]
