from django.contrib import admin
from .models import Author, Book # Importing Author and Book models

# Registering Author and Book models with the admin site
admin.site.register(Author)
admin.site.register(Book)
