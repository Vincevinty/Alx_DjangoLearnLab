from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer


# --- Book API Views using GenericAPIView Subclasses ---

class BookListView(generics.ListAPIView): # View for listing all books
    """
    API view for listing books, supporting filtering, searching, and ordering.
    
    Query Parameters:
    - Filtering: ?title=<value>, ?author=<ID>, ?publication_year=<year>
    - Searching: ?search=<text> (searches title and author name)
    - Ordering: ?ordering=<field> (orders by title or publication_year)
    """
    queryset = Book.objects.all() # Queryset to retrieve all Book instances
    serializer_class = BookSerializer  # Serializer class to convert Book instances to JSON
    permission_classes = [permissions.AllowAny] # Allow any user (authenticated or not) to access this view
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter, 
        filters.OrderingFilter
        ]  # Enable filtering, searching, and ordering backends
    filterset_fields = ['title', 'author', 'publication_year']  # Fields to filter by: title, author (ID), and publication year
    # Refined search field to target the author's name (assuming 'name' field on Author model)
    search_fields = ['title', 'author__name']  # Enable search on book title and author's name
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
        serializer.save() # Save the new book instance

class BookUpdateView(generics.UpdateAPIView): # View for updating an existing book
    queryset = Book.objects.all() # Queryset to retrieve all Book instances
    serializer_class = BookSerializer # Serializer class to convert Book instances to JSON
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can update

    def perform_update(self, serializer): # Custom behavior on update
        serializer.save() # Save the updated book instance

class BookDeleteView(generics.DestroyAPIView): # View for deleting a book
    queryset = Book.objects.all() # Queryset to retrieve all Book instances
    serializer_class = BookSerializer # Serializer class to convert Book instances to JSON
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can delete

    def perform_destroy(self, instance): # Custom behavior on deletion
        instance.delete() # Delete the book instance
