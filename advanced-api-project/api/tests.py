# api/tests.py - Corrected setup for Book and Author instances

from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

# Assuming your models are located here:
from .models import Book, Author 

User = get_user_model()

class BookAPITestCase(APITestCase):
    """
    Test suite for the Book API endpoints.
    
    The original error: 
    'ValueError: Cannot assign "'Bram Stoker'": "Book.author" must be a "Author" instance.'
    is fixed by creating an Author instance first and passing that object to the Book creation.
    """
    def setUp(self):
        # --- FIX STARTS HERE ---
        # 1. Create a User for authenticated tests
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.force_authenticate(user=self.user)
        
        # 2. Create an Author instance FIRST
        self.author = Author.objects.create(name='Bram Stoker') 
        self.other_author = Author.objects.create(name='Jane Austen')

        # 3. Use the Author instance in the book data for creation
        self.book_data = {
            'title': 'Dracula',
            'publication_date': '1897-05-26',
            'isbn': '978-0199537151',
            # CRITICAL FIX: Pass the Author instance (self.author), not a string
            'author': self.author, 
        }

        # 4. Now creating the book instance works correctly
        self.book = Book.objects.create(**self.book_data) # Creating a book instance for testing
        
        # Set up URLs for convenience
        self.list_url = reverse('book-list')
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book.pk})
        
        # Data structure for authenticated POST request (must use author ID for serializer)
        self.new_book_payload = {
            'title': 'Frankenstein',
            'publication_date': '1818-01-01',
            'isbn': '978-0141439471',
            # For API POST/PUT requests, the serializer expects the Author's primary key (ID)
            'author': self.author.id, 
        }
        

    def test_list_books(self):
        """Test retrieving the list of books."""
        # Note: Unauthenticated users should usually be allowed to view lists
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Dracula')

    def test_create_book_authenticated(self):
        """Test creating a book with an authenticated user."""
        response = self.client.post(self.list_url, self.new_book_payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(response.data['title'], 'Frankenstein')

    def test_create_book_unauthenticated(self):
        """Test creating a book without authentication (should fail with 403)."""
        self.client.force_authenticate(user=None)
        response = self.client.post(self.list_url, self.new_book_payload, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Book.objects.count(), 1) # Should not have created a new book

    def test_update_book(self):
        """Test updating an existing book."""
        update_data = {
            'title': 'Dracula Updated',
            'publication_date': '1897-05-26',
            'isbn': '978-0199537151',
            'author': self.author.id,
        }
        response = self.client.put(self.detail_url, update_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Dracula Updated')

    def test_delete_book(self):
        """Test deleting a book."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Book.objects.count(), 0)

    # Example tests for filtering and ordering (assuming your ViewSet supports them)

    def test_filter_books_by_author(self):
        """Test filtering books by author ID."""
        Book.objects.create(
            title='Pride and Prejudice', 
            publication_date='1813-01-28', 
            isbn='1234567890', 
            author=self.other_author # Use the other author instance
        )
        
        # Filter for 'Bram Stoker' (self.author.id)
        response = self.client.get(f'{self.list_url}?author_id={self.author.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Dracula')

    def test_search_books(self):
        """Test searching books by title or ISBN."""
        # Note: This test assumes your ViewSet has a search field defined
        # Example: search=Dracula
        response = self.client.get(f'{self.list_url}?search=Drac')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Dracula')

    def test_order_books_by_title(self):
        """Test ordering books by title (e.g., in descending order)."""
        Book.objects.create(
            title='Zzz', 
            publication_date='2000-01-01', 
            isbn='0000', 
            author=self.author
        )
        # Note: This test assumes your ViewSet has ordering enabled
        response = self.client.get(f'{self.list_url}?ordering=-title')
        self.assertEqual(response.status_code, 200)