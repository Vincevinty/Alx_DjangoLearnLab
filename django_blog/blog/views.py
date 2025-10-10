from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm

# --- Placeholder View for Main Blog Content ---
def post_list(request):
    """
    Placeholder view for the main blog page (the root URL).
    This view will eventually list all blog posts.
    """
    context = {
        'title': 'Welcome to the Django Blog',
        'is_authenticated': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else 'Guest'
    }
    # NOTE: You will need to create 'blog/templates/post_list.html' later.
    return render(request, 'post_list.html', context)

# --- Authentication Views ---

def register(request):
    """
    View function to handle user registration.
    Uses the CustomUserCreationForm (from blog/forms.py).
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account created for {form.cleaned_data.get("username")}! You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    """
    View function to display and manage the user profile.
    Handles POST request to update the user's email address.
    """
    # Handles form submission to update the user's email
    if request.method == 'POST':
        # Safely retrieve the new email from the POST data
        new_email = request.POST.get('email', '').strip()

        if new_email and new_email != request.user.email:
            # Check if the new email already exists (excluding the current user's email)
            if User.objects.filter(email=new_email).exclude(pk=request.user.pk).exists():
                messages.error(request, 'This email is already associated with another account.')
            else:
                # Update and save the user object
                request.user.email = new_email
                request.user.save()
                messages.success(request, 'Your email address has been successfully updated.')
        elif new_email == request.user.email:
             messages.info(request, 'No changes were made to your email address.')
        else:
             messages.error(request, 'The email field cannot be empty.')
             
        # Redirect back to the profile page (GET request) to prevent form resubmission
        return redirect('profile')

    # Handles initial page load (GET request)
    return render(request, 'profile.html', {'user': request.user})