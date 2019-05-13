from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from tracker import urls
from . import views

urlpatterns = [
    path('', views.home, name='users-home'),
    path('register/', views.register, name='users-register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='users-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='login.html'), name='users-logout'),
    path('reset/', auth_views.PasswordResetView.as_view(template_name='reset.html', extra_context={'email': 'email'}), name='password_reset'),
    path('reset/done', auth_views.PasswordResetDoneView.as_view(template_name='reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reset.html', post_reset_login=True, success_url=reverse_lazy('tracker-home')), name='password_reset_confirm'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]
