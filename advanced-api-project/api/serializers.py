from rest_framework import serializers # Importing serializers from Django REST framework
from .models import Author, Book # Importing Author and Book models
from datetime import datetime # Importing datetime module for date validation

class BookSerializer(serializers.ModelSerializer): # Serializer for the Book model
    class Meta: # Meta class to define model and fields
        model = Book # Specifies the model to be serialized
        fiels = '__all__' # Serializes all fields of the Book model

    def validate_publication_year(self, value): # Custom validation for publication_year field
        current_year = datetime.now().year # Gets the current year
        if value > current_year: # Checks if the publication year is not the future
            raise serializers.ValidationError("Publication year cannot be in the future.") # Raises validation error
        return value # Returns the validated value
    
class AuthorSerializer(serializers.ModelSerializer):  # Serializer for the Author model
    books = BookSerializer(many=True, read_only=True)  # Nested serializer for related books

    class Meta:  # Meta class to define model and fields
        model = Author  # Specifies the model to be serialized
        fields = ['name', 'books']  # Specifies the fields to be included in the serialization
        
    def validate_name(self, value): # Custom validation for name field
        if not value.strip(): # Checks if the name is empty or only whitespace
            raise serializers.ValidationError("Author name cannot be empty.") # Raises validation error
        return value # Returns the validated value