from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Book, Author
from rest_framework import status

User = get_user_model()

class BookViewTests(APITestCase):
    """
    Test suite for the Book API endpoints (List, Detail, Create, Update, Delete)
    with a focus on advanced querying and permissions.
    """
    def setUp(self):
        # --- Authentication Setup ---
        self.user = User.objects.create_user(username='admin_user', password='password')
        self.non_auth_client = self.client # Client without forced authentication

        # --- Data Setup: Authors ---
        self.author_stoker = Author.objects.create(name='Bram Stoker')
        self.author_janeausten = Author.objects.create(name='Jane Austen')

        # --- Data Setup: Books ---
        self
        self.book_a = Book.objects.create(
            title='Dracula',
            author=self.author_stoker,
            publication_year=1897,
            isbn='1234567890123'
        )
        self.book_b = Book.objects.create(
            title='Pride and Prejudice',
            author=self.author_janeausten,
            publication_year=1813,
            isbn='9876543210987'
        )
        self.book_c = Book.objects.create(
            title='Northanger Abbey',
            author=self.author_janeausten,
            publication_year=1817,
            isbn='1111111111111'
        )

        # --- URL Setup ---
        # Assuming the following URL names correspond to your generic views:
        self.list_create_url = reverse('book-list') # Maps to BookListView (GET) and BookCreateView (POST)
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book_a.pk}) # Maps to BookDetailView/UpdateView/DeleteView

        # --- Payload for Creation/Update ---
        self.valid_payload = {
            'title': 'The Great Gatsby',
            'publication_year': 1925,
            # Pass the author ID for the ForeignKey field
            'author': self.author_stoker.id,
        }
        self.invalid_payload = {
            'title': 'Missing Author'
            # Missing required 'publication_year' and 'author'
        }


    # ======================================================================
    # 1. CRUD Operation Tests (Functionality & Permissions)
    # ======================================================================

    def test_list_books_succeeds_for_any_user(self):
        """Test GET (List) /books/ is accessible by anyone."""
        response = self.non_auth_client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_retrieve_book_succeeds_for_any_user(self):
        """Test GET (Detail) /books/<pk>/ is accessible by anyone."""
        response = self.non_auth_client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Dracula')

    def test_create_book_authenticated(self):
        """Test POST (Create) /books/ requires authentication and succeeds."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_create_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)

    def test_create_book_unauthenticated_fails(self):
        """Test POST (Create) /books/ fails for unauthenticated users."""
        response = self.non_auth_client.post(self.list_create_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 3)

    def test_update_book_authenticated(self):
        """Test PUT (Update) /books/<pk>/ requires authentication and succeeds."""
        self.client.force_authenticate(user=self.user)
        update_data = self.valid_payload.copy()
        update_data['title'] = 'Dracula: Revised Edition'
        response = self.client.put(self.detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book_a.refresh_from_db()
        self.assertEqual(self.book_a.title, 'Dracula: Revised Edition')

    def test_delete_book_unauthenticated_fails(self):
        """Test DELETE (Destroy) /books/<pk>/ fails for unauthenticated users."""
        response = self.non_auth_client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 3)

    # ======================================================================
    # 2. Advanced Querying Tests (Filtering, Searching, Ordering)
    # ======================================================================

    def test_filter_by_publication_year(self):
        """Test filtering by the 'publication_year' field."""
        # GET /api/books/?publication_year=1813
        response = self.client.get(f'{self.list_create_url}?publication_year=1813')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Pride and Prejudice')

    def test_filter_by_author_id(self):
        """Test filtering by the 'author' ForeignKey ID."""
        # GET /api/books/?author=<Jane Austen ID>
        response = self.client.get(f'{self.list_create_url}?author={self.author_janeausten.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Check if both Jane Austen books are present (order isn't guaranteed here)
        titles = {book['title'] for book in response.data}
        self.assertIn('Pride and Prejudice', titles)
        self.assertIn('Northanger Abbey', titles)

    def test_search_by_title_keyword(self):
        """Test searching by a keyword in the 'title' field."""
        # GET /api/books/?search=Prejudice
        response = self.client.get(f'{self.list_create_url}?search=Prejudice')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Pride and Prejudice')

    def test_search_by_author_name_keyword(self):
        """Test searching by a keyword in the related 'author__name' field."""
        # GET /api/books/?search=Austen
        response = self.client.get(f'{self.list_create_url}?search=Austen')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_ordering_by_title_descending(self):
        """Test ordering the results by title descending (-title)."""
        # Titles are: Dracula, Pride and Prejudice, Northanger Abbey
        # Ordered descending should be: Pride and Prejudice, Northanger Abbey, Dracula
        # Note: Python string ordering makes 'N' (Northanger) appear before 'P' (Pride), let's sort by year instead for clarity.
        
        # Order by title descending: Pride and Prejudice, Northanger Abbey, Dracula
        response = self.client.get(f'{self.list_create_url}?ordering=-title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Pride and Prejudice')
        self.assertEqual(response.data[1]['title'], 'Northanger Abbey')
        self.assertEqual(response.data[2]['title'], 'Dracula')

    def test_ordering_by_publication_year_ascending(self):
        """Test ordering the results by publication_year ascending."""
        # Years are: 1897, 1813, 1817
        # Ordered ascending: 1813, 1817, 1897
        response = self.client.get(f'{self.list_create_url}?ordering=publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 1813) # Pride and Prejudice
        self.assertEqual(response.data[1]['publication_year'], 1817) # Northanger Abbey
        self.assertEqual(response.data[2]['publication_year'], 1897) # Dracula