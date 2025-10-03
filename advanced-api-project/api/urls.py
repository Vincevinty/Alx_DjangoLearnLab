from django.urls import path, include
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView, 
    BookUpdateView,
    BookDeleteView
)

urlspatterns = [
    path('books/', BookListView.as_view(), name='book-list'), # URL for listing all books
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'), # URL for book details
    path('books/create/', BookCreateView.as_view(), name='book-create'), # URL for creating a new book
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'), # URL for updating a book
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'), # URL for deleting a book
]