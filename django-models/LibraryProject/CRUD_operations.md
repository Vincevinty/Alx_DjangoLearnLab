# CRUD Operations for Book Model.

## Create
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year="1949")
book

## Retrieve
book = Book.objects.get(title="1984")
book.title, book.author, book.publication_year

## Update
book.title = "Nineteen Eighty-Four"
book.save()
book.title

## Delete
book.delete()
Book.objects.all()
