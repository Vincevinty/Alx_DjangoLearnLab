from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Extends the default UserCreationForm to explicitly include the email field.
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        # Use the default User model
        model = User
        # Include all default fields (username, password, password2) plus email
        fields = ('username', 'email') + UserCreationForm.Meta.fields[2:]

    def clean_email(self): # Custom validation for the email field
        email = self.cleaned_data.get('email') # Get the email from the cleaned data
        if User.objects.filter(email=email).exists(): # Check if a user with this email already exists
            raise forms.ValidationError("A user with that email already exists.") # Raise a validation error if the email is already taken
        return email # Return the cleaned email if it's valid