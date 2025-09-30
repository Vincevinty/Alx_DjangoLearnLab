from .models import Author, Book
from rest_framework import serializers
from datetime import date

# BookSerializer converts Book model instances to and from JSON format.
# It includes all fields and adds validation to ensure the publication date is not in the future.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__' # Includes all fields of the Book model

def validate_publication_year(self, value): # Custom validation to ensure publication_date is not set in the future
    if value > date.today():
        raise serializers.ValidationError("Publication year cannot be in the future.")
    return value

# AuthorSerializer converts Author model instances to and from JSON format.
# It includes all fields and nests the related BookSerializer to show all books by the author.
class AuthorSerializer(serializers.ModelSerializer):
    book = BookSerializer(many = True, read_only = True) #Nested serialization to include all books by the author
    class Meta:
        model = Author
        fields = ['name', 'book'] # Includes author's name and their books

def validate_name(self, value): # Custom validation to ensure author's name is not empty and has a minimum length
    if not value.strip():
        raise serializers.ValidationError("Author name cannot be empty or just spaces.")
    if len(value) < 3:
        raise serializers.ValidationError("Author name must be at least 3 characters long.")    
    return value 