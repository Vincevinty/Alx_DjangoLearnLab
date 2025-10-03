from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Book, Author

class BookAPITestCase(APITestCase): # Test case for Book API endpoints
    def setUp(self): # Setup method to initialize test data
        self.user = User.objects.create_user(username='testuser', password='testpass') # Create a test user
        self.client = APIClient() # Initialize the APIClient
        self.book_data = {
            'title': 'Dracula',
            'author': 'Bram Stoker',
            'publication_year': 1897
        } # Sample book data for testing
        self.book = Book.objects.create(**self.book_data) # Creating a book instance for testing

    def test_create_book_authenticated(self): # Test creating a book with authentication
        self.client.force_authenticate(user=self.user) # Authenticating the user
        response = self.client.post('/books/create/', {
            'title': 'Frankenstein',
            'author': 'Mary Shelley',
            'publication_year': 1818
        }) # Creating a new book
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # Check if creation is successful
        self.assertEqual(response.data['title'], 'Frankenstein') # Check if the book title is correct

    def test_create_book_unauthenticated(self): # Test creating a book without authentication
        response = self.client.post('/books/create/', self.book_data) # Attempting to create without authentication
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) # Unauthenticated users should not be able to create

    def test_update_book(self): # Test updating a book
        self.client.force_authenticate(user=self.user) # Authenticating the user
        response = self.client.put(f'/books/{self.book.id}/update/', {
            'title': 'Dracula Revised',
            'author': 'Bram Stoker',
            'publication_year': 1897
        }) # Updating the book
        self.assertEqual(response.status_code, status.HTTP_200_OK) # Check if update is successful
        self.assertEqual(response.data['title'], 'Dracula Revised') # Check if the title is updated

    def test_delete_book(self): # Test deleting a book
        self.client.force_authenticate(user=self.user) # Authenticating the user
        response = self.client.delete(f'/books/{self.book.id}/delete/') # Deleting the book
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) # Check if deletion is successful
        self.assertFalse(Book.objects.filter(id=self.book.id).exists()) # Ensure the book is deleted

    def test_filter_books_by_author(self): # Test filtering books by author
        response = self.client.get('/books/?author=Bram Stoker') # Filtering by author
        self.assertEqual(response.status_code, status.HTTP_200_OK) # Check if filtering is successful
        self.assertEqual(response.data[0]['author'], 'Bram Stoker') # Check if filtering by author works

    def test_search_books(self): # Test searching books by title
        response = self.client.get('/books/?search=Drac') # Searching for 'Drac' in title
        self.assertEqual(response.status_code, status.HTTP_200_OK) # Check if search is successful
        self.assertIn('Dracula', response.data[0]['title']) # Check if search returns the correct book

    def test_order_books_by_title(self): # Test ordering books by title
        Book.objects.create(title='A Tale of Two Cities', author='Charles Dickens', publication_year=1859) # Adding another book for ordering test
        response = self.client.get('/books/?ordering=title') # Ordering by title
        self.assertEqual(response.status_code, status.HTTP_200_OK) # Check if books are ordered by title
        titles = [book['title'] for book in response.data] # Extract titles from response
        self.assertEqual(titles, sorted(titles)) # Check if titles are in ascending order

class BookAPITestCase(APITestCase): # Test case for Book API endpoints
    def setUp(self): # Setup method to initialize test data
        self.user = User.objects.create_user(username='testuser', password='testpass') # Create a test user
        self.client = APIClient() # Initialize the APIClient

        # Create an Author instance
        self.author = Author.objects.create(name='Bram Stoker') 

        # Use the Author instance, not a string
        self.book_data = {
            'title': 'Dracula',
            'author': self.author,
            'publication_year': 1897
        } 

        self.book = Book.objects.create(**self.book_data) # Creating a book instance for testing