from django.shortcuts import render
from rest_framework import generics
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

class BookUpdateView(generics.UpdateApiView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDeleteView(generics.DestroyApiView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer