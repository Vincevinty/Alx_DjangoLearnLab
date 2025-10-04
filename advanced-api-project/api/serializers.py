from rest_framework import serializers
from .models import Book, Author

# --- Fix 1: Serializer Assertion Error ---
# The assertion error "Add an explicit fields = '__all__' to the BookSerializer serializer" 
# is fixed by adding fields = '__all__'.

class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for the Author model."""
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    The 'author' field is inherited from the ModelSerializer and will expect 
    the Author ID on write operations (POST/PUT).
    """
    class Meta:
        model = Book
        # MANDATORY FIX: Explicitly define fields to resolve DRF AssertionError
        fields = '__all__'
        read_only_fields = ('id',)