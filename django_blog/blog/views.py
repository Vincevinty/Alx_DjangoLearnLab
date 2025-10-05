from django.shortcuts import render
from django.contrib.auth.models import User

def register_user(request): # view function to register a new user
    user = User(username='AwonkeVintwembi',) # create a new user instance
    user.set_password('secure_password')  # hashes it
    user.save() # save the user to the database

