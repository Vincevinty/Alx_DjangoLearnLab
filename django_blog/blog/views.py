from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm


def register_user(request): # view function to register a new user
    user = User(username='AwonkeVintwembi',) # create a new user instance
    user.set_password('secure_password')  # hashes it
    user.save() # save the user to the database

def register(request): # view function to handle user registration
    if request.method == 'POST': # Check if the request method is POST
        form = CustomUserCreationForm(request.POST) # Instantiate the form with POST data
        if form.is_valid(): # Check if the form is valid
            form.save() # Save the new user to the database
            return redirect('login')  # Redirect to login page after successful registration
    else: # If the request method is not POST
        form = CustomUserCreationForm() # Instantiate an empty form
    return render(request, 'register.html', {'form': form}) # Render the registration template with the form

@login_required # Ensure the user is logged in to access this view
def profile(request): # view function to display user profile
    if request.method == 'POST': # Check if the request method is POST
        new_email = request.Post.get('email') # Get the new email from the POST data
    if new_email: # If a new email is provided
        request.user.email = new_email # Update the user's email
        request.user.email = request.POST.get('email') # Update the user's email
        request.user.save() # Save the updated user information
    return render(request, 'profile.html', {'user': request.user}) # Render the profile template with the user context