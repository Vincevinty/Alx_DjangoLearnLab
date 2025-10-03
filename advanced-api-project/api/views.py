from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import BookSerializer
from .models import Book    

class BookListView(generics.ListApiView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetailView(generics.RtrieveApiView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer   

class BookCreateView(generics.CreateApiView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can create

    def perform_create(self, serializer): # Custom behavior on creation
        # Example: attach the current user as the creator if your model supports it
        serializer.save() # Save the new book instance

class BookUpdateView(generics.UpdateApiView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can update

    def perform_update(self, serializer): # Custom behavior on update
        # You can add custom logic here, like logging or conditional updates
        serializer.save() # Save the updated book instance

class BookDeleteView(generics.DestroyApiView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer