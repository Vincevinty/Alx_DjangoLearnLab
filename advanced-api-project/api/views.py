from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Book # Assuming you have a Book model
from .serializers import BookSerializer # Assuming you have a BookSerializer

class BookListCreateView(generics.ListCreateAPIView):
    """
    Handles GET (list) and POST (create) requests for Book model.

    - Uses ListCreateAPIView to handle both operations at the /books/ endpoint.
    - Permissions: GET is public; POST requires authentication.
    - Implements filtering, searching, and ordering.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Permission Fix: Allows GET (list) for everyone, but requires 
    # authentication for POST (create). This resolves the 403 errors in tests.
    permission_classes = [IsAuthenticatedOrReadOnly] 
    
    # Advanced Querying Backends: Required for the filtering, search, and ordering tests.
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Filtering fields: Used for '?publication_year=...' and '?author=...'
    filterset_fields = ['publication_year', 'author']

    # Searching fields: Used for '?search=...' (searches title and author name)
    search_fields = ['title', 'author__name']

    # Ordering fields: Used for '?ordering=...'
    ordering_fields = ['title', 'publication_year']
    
    # Default ordering to ensure consistent pagination/listing
    ordering = ['id']


class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles GET (retrieve), PUT/PATCH (update), and DELETE (destroy) requests for a single Book.
    
    - Uses RetrieveUpdateDestroyAPIView to handle all operations at the /books/<pk>/ endpoint.
    - Permissions: GET is public; PUT/PATCH/DELETE require authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer 
    
    # Permission Fix: Allows GET (retrieve) for everyone, but requires 
    # authentication for PUT, PATCH, and DELETE.
    permission_classes = [IsAuthenticatedOrReadOnly] # Resolves 403 errors in tests