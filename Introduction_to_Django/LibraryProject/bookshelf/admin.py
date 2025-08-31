from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Columns shown in admin list view
    search_fields = ('title', 'author')                     # Enables search box
    list_filter = ('publication_year',)                     # Adds sidebar filter

admin.site.register(Book, BookAdmin) # Register the Book model with the custom admin interface
