from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'), # User registration view
    path('profile/', views.profile, name='profile'), # User profile view
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'), # Custom login view
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'), # Redirect to login page after logout
]