from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView, 
    BookUpdateView,
    BookDeleteView,
)

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'), # Added URL pattern for listing all books
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'), # Added URL pattern for book details
    path('books/create/', BookCreateView.as_view(), name='book-create'), # Added URL pattern for creating a book
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'), # Added URL pattern for updating a book
    path('books/update/', BookUpdateView.as_view()), # Added URL pattern for updating a book
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),  # Added URL pattern for deleting a book
    path('books/delete/', BookDeleteView.as_view()), # Added URL pattern for deleting a book
    # Endpoint for GET (List) and POST (Create)
    # The name='book-list' is used for reverse URL matching in tests and elsewhere
    path('books/', BookListCreateView.as_view(), name='book-list'), 
    path('books/<int:pk>/', BookRetrieveUpdateDestroyView.as_view(), name='book-detail'),
]
