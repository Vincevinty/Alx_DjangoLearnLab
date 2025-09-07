from django.shortcuts import render
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView

# Function-based view to list all books
def list_books(request):
   books = Book.objects.all()  # This is the missing line
   return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view to show book details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'