from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views

# This file handles all URLs prefixed with 'users/' 
urlpatterns = [
    # Custom views defined in blog/views.py
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    
    # Built-in Django authentication views (Login/Logout)
    # The 'login' name is used by default by Django's auth system for redirects
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    
    # After logging out, the user is redirected back to the login page
    path('logout/', auth_views.LogoutView.as_view(next_page='/users/login/'), name='logout'),
]