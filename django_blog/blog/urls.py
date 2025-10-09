from django.contrib.auth import auth_views
from django.urls import path

path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),