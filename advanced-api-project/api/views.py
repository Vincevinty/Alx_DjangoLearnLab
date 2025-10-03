from django.shortcuts import render
from rest_framework import generics, permissions, filters
from .serializers import BookSerializer
from .models import Book
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend



class BookListView(generics.ListAPIView): # View for listing all books
    queryset = Book.objects.all() # Queryset to retrieve all Book instances
    serializer_class = BookSerializer  # Serializer class to convert Book instances to JSON
    permission_classes = [permissions.AllowAny] # Allow any user (authenticated or not) to access this view
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter, 
        filters.OrderingFilter
        ]  # Enable filtering backend
    filterset_fields = ['title', 'author', 'publication_year']  # Fields to filter by: title, author, and publication year
    search_fields = ['title', 'author']  # Enable search on title and author's name
    ordering_fields = ['title', 'publication_year'] # Allow ordering by title and publication year
    ordering = ['title']  # Default ordering by title
class BookDetailView(generics.RetrieveAPIView): # View for retrieving a single book by its ID
    queryset = Book.objects.all() # Queryset to retrieve all Book instances
    serializer_class = BookSerializer # Serializer class to convert Book instances to JSON
    permission_classes = [permissions.AllowAny]  # Allow any user (authenticated or not) to access this view



class BookCreateView(generics.CreateAPIView): # View for creating a new book
    queryset = Book.objects.all() # Queryset to retrieve all Book instances
    serializer_class = BookSerializer # Serializer class to convert Book instances to JSON
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can create

    def perform_create(self, serializer): # Custom behavior on creation
        # Example: attach the current user as the creator if your model supports it
        serializer.save() # Save the new book instance

class BookUpdateView(generics.UpdateAPIView): # View for updating an existing book
    queryset = Book.objects.all() # Queryset to retrieve all Book instances
    serializer_class = BookSerializer # Serializer class to convert Book instances to JSON
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can update

    def perform_update(self, serializer): # Custom behavior on update
        # You can add custom logic here, like logging or conditional updates
        serializer.save() # Save the updated book instance

class BookDeleteView(generics.DestroyAPIView): # View for deleting a book
    queryset = Book.objects.all() # Queryset to retrieve all Book instances
    serializer_class = BookSerializer # Serializer class to convert Book instances to JSON
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can delete

    def perform_destroy(self, instance): # Custom behavior on deletion
        # You can add custom logic here, like logging deletions
        instance.delete() # Delete the book instance