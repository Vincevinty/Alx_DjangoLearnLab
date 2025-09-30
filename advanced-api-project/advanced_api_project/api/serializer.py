from .models import Author, Book
from rest_framework import serializers
from datetime import date

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

def validate_publication_year(self, value):
    if value > date.today():
        raise serializers.ValidationError("Publication year cannot be in the future.")
    return value

class AuthorSerializer(serializers.ModelSerializer):
    book = BookSerializer(many = True, read_only = True) #Nested serialization

    class Meta:
        model = Author
        fields = ['name', 'book']

def validate_name(self, value):
    if not value.strip():
        raise serializers.ValidationError("Author name cannot be empty or just spaces.")
    if len(value) < 3:
        raise serializers.ValidationError("Author name must be at least 3 characters long.")    
    return value 