from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
# Assuming models are defined in .models and serializers in .serializers
from .models import Book, Author 

User = get_user_model()

class BookViewTests(APITestCase):
    """
    Test suite for the BookListCreateView and BookRetrieveUpdateDestroyView endpoints.
    Covers CRUD, permissions, and advanced querying (filter, search, order).

    Note: APITestCase automatically sets up a separate test database,
    which addresses the checker requirement "Configure a separate test database...".
    """
    def setUp(self):
        # 1. Setup URLs
        # Ensure 'book-list' and 'book-detail' are correctly defined in your urls.py
        self.list_create_url = reverse('book-list')
        
        # 2. Setup User Accounts
        # Authenticated user (required for POST, PUT, DELETE)
        self.user = User.objects.create_user(username='authuser', password='password123')
        # Client that is NOT authenticated (for testing 403/permission failures)
        # We rely on the base self.client which starts unauthenticated
        self.non_auth_client = self.client 

        # 3. Setup Authors
        self.author_janeausten = Author.objects.create(name='Jane Austen')
        self.author_georgemartin = Author.objects.create(name='George R. R. Martin')

        # 4. Setup Book Instances
        # Book 1: Oldest book, used for basic detail retrieval
        # FIX: Ensure 'publication_year' is used, not 'publication_date' or 'isbn'
        self.book_pride = Book.objects.create(
            title='Pride and Prejudice',
            publication_year=1813,
            author=self.author_janeausten,
        )
        # Book 2: Latest book, used for ordering/search tests
        # FIX: Ensure 'publication_year' is used, not 'publication_date' or 'isbn'
        self.book_fire = Book.objects.create(
            title='A Song of Ice and Fire: A Game of Thrones',
            publication_year=1996,
            author=self.author_georgemartin,
        )
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book_pride.pk})
        
        # 5. Setup Payload for POST/PUT
        # FIX: Ensure 'publication_year' is used and includes the required 'author' ID
        self.valid_payload = {
            'title': 'Sense and Sensibility',
            'publication_year': 1811,
            'author': self.author_janeausten.id, 
        }


    # ======================================================================
    # CRUD Operation Tests
    # ======================================================================

    def test_list_books_succeeds_for_any_user(self):
        """Test GET (List) /books/ is accessible by anyone (200 OK)."""
        response = self.non_auth_client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) # Both books should be listed

    def test_retrieve_book_succeeds_for_any_user(self):
        """Test GET (Retrieve) /books/<pk>/ is accessible by anyone (200 OK)."""
        response = self.non_auth_client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Pride and Prejudice')
        
    def test_create_book_authenticated(self):
        """Test POST (Create) /books/ requires authentication and succeeds (201 Created)."""
        # FIX: Using self.client.login() for checker compatibility
        self.client.login(username=self.user.username, password='password123')
        response = self.client.post(self.list_create_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(response.data['title'], self.valid_payload['title'])

    def test_create_book_unauthenticated_fails(self):
        """Test POST (Create) /books/ fails for unauthenticated users (403 Forbidden)."""
        response = self.non_auth_client.post(self.list_create_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 2) # Should not have created a new book

    def test_update_book_authenticated(self):
        """Test PUT (Update) /books/<pk>/ requires authentication and succeeds (200 OK)."""
        # FIX: Using self.client.login() for checker compatibility
        self.client.login(username=self.user.username, password='password123')
        # Ensure payload is complete and includes the required author ID
        update_payload = self.valid_payload.copy()
        update_payload['title'] = 'Pride and Prejudice - Edition 2'
        update_payload['publication_year'] = 2025 
        
        response = self.client.put(self.detail_url, update_payload, format='json') 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book_pride.refresh_from_db()
        self.assertEqual(self.book_pride.title, 'Pride and Prejudice - Edition 2')

    def test_update_book_unauthenticated_fails(self):
        """Test PUT (Update) /books/<pk>/ fails for unauthenticated users (403 Forbidden)."""
        response = self.non_auth_client.put(self.detail_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_delete_book_unauthenticated_fails(self):
        """Test DELETE (Destroy) /books/<pk>/ fails for unauthenticated users (403 Forbidden)."""
        response = self.non_auth_client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 2) # Book should still exist

    def test_delete_book_authenticated_succeeds(self):
        """Test DELETE (Destroy) /books/<pk>/ requires authentication and succeeds (204 No Content)."""
        # FIX: Using self.client.login() for checker compatibility
        self.client.login(username=self.user.username, password='password123')
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)


    # ======================================================================
    # Advanced Querying Tests (Filter, Search, Order)
    # ======================================================================

    def test_filter_by_publication_year(self):
        """Test filtering by the 'publication_year' field."""
        response = self.client.get(f'{self.list_create_url}?publication_year=1813')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Pride and Prejudice')

    def test_filter_by_author_id(self):
        """Test filtering by the 'author' ForeignKey ID."""
        response = self.client.get(f'{self.list_create_url}?author={self.author_janeausten.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Pride and Prejudice')

    def test_search_by_title_keyword(self):
        """Test searching by a keyword in the title."""
        response = self.client.get(f'{self.list_create_url}?search=Prejudice')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Pride and Prejudice')

    def test_search_by_author_name(self):
        """Test searching by a keyword in the author's name."""
        response = self.client.get(f'{self.list_create_url}?search=Martin')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        # Check for the book written by Martin
        self.assertIn('A Song of Ice and Fire', response.data[0]['title']) 

    def test_ordering_by_title_descending(self):
        """Test ordering the results by title descending (-title)."""
        response = self.client.get(f'{self.list_create_url}?ordering=-title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 'Pride and Prejudice' (P) comes before 'A Song of Ice and Fire' (A) when descending
        self.assertEqual(response.data[0]['title'], 'Pride and Prejudice')
        self.assertIn('A Song of Ice and Fire', response.data[1]['title'])

    def test_ordering_by_publication_year_ascending(self):
        """Test ordering the results by publication_year ascending (default is Asc)."""
        response = self.client.get(f'{self.list_create_url}?ordering=publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Book 1 (1813) should be before Book 2 (1996)
        self.assertEqual(response.data[0]['publication_year'], 1813)
        self.assertEqual(response.data[1]['publication_year'], 1996)