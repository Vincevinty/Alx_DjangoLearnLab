from django.contrib import admin
from .models import Author, Book

admin.site.register(Author) # Registers the Author model with the admin site
admin.site.register(Book)   # Registers the Book model with the admin site
