from django.shortcuts import render
from .models import Book
from django.contrib.auth.decorators import permission_required
from django import forms
from .forms import ExampleForm

@permission_required('bookshelf.view_book', raise_exception=True)

def book_list(request):
    books = Book.objects.all()
    query = request.GET.get('q', '')
    books = Book.objects.filter(title__icontains=query)
    return render(request, 'bookshelf/book_list.html', {'books': books})

class BookSearchForm(forms.Form):
    q = forms.CharField(max_length=100)

def example_view(request):
    form = ExampleForm(request.POST or None)
    if form.is_valid():
        # process form data
        pass
    return render(request, 'bookshelf/example_form.html', {'form': form})




