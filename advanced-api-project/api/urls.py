from django.urls import path
# FIX: The import names must match the class names in api/views.py
from .views import BookListCreateView, BookRetrieveUpdateDestroyView

urlpatterns = [
    # Consolidated endpoint for GET (List) and POST (Create).
    # This single path handles listing all books and creating a new book.
    path('books/', BookListCreateView.as_view(), name='book-list'), 
    
    # Consolidated endpoint for GET (Retrieve), PUT/PATCH (Update), and DELETE (Destroy).
    # This single path handles all detail-related operations on a book by primary key (pk).
    path('books/<int:pk>/', BookRetrieveUpdateDestroyView.as_view(), name='book-detail'),
]
