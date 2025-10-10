from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm

# --- Blog Content Views ---

def post_list(request):
    """
    Placeholder for the main blog list view.
    This view handles the root path ('/').
    """
    context = {
        'posts': [
            {'title': 'Welcome to Django Blog', 'author': 'Awonke', 'date': '2025-10-10'},
            {'title': 'Setting up Authentication', 'author': 'User', 'date': '2025-10-12'}
        ],
        'title': 'Blog Home'
    }
    return render(request, 'post_list.html', context)

# --- Authentication Views ---

def register(request):
    """
    View function to handle user registration using the CustomUserCreationForm.
    Redirects to the login page on successful registration.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the new user, email uniqueness is checked in forms.py
            user = form.save()
            messages.success(request, f'Account created for {user.username}! Please log in.')
            return redirect('login') 
        else:
            messages.error(request, 'Registration failed. Please check the errors below.')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'register.html', {'form': form, 'title': 'Register'})

@login_required 
def profile(request):
    """
    View function to display the user profile and allow email updates.
    Ensures only authenticated users can access the view.
    """
    if request.method == 'POST':
        new_email = request.POST.get('email')
        
        if new_email:
            # Check if email is already in use by another user (excluding the current user)
            if User.objects.filter(email=new_email).exclude(pk=request.user.pk).exists():
                messages.error(request, 'That email is already registered to another user.')
            else:
                request.user.email = new_email
                request.user.save()
                messages.success(request, 'Your profile has been updated successfully!')
        else:
            messages.error(request, 'Email field cannot be empty.')
            
    # Render the profile page with the current user's context
    return render(request, 'profile.html', {'user': request.user, 'title': 'Profile'})