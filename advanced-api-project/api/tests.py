from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Book

class BookAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.book_data = {
            'title': 'Dracula',
            'author': 'Bram Stoker',
            'publication_year': 1897
        }
        self.book = Book.objects.create(**self.book_data)

    def test_create_book_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/books/create/', {
            'title': 'Frankenstein',
            'author': 'Mary Shelley',
            'publication_year': 1818
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Frankenstein')

    def test_create_book_unauthenticated(self):
        response = self.client.post('/books/create/', self.book_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(f'/books/{self.book.id}/update/', {
            'title': 'Dracula Revised',
            'author': 'Bram Stoker',
            'publication_year': 1897
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Dracula Revised')

    def test_delete_book(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/books/{self.book.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    def test_filter_books_by_author(self):
        response = self.client.get('/books/?author=Bram Stoker')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['author'], 'Bram Stoker')

    def test_search_books(self):
        response = self.client.get('/books/?search=Drac')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Dracula', response.data[0]['title'])

    def test_order_books_by_title(self):
        Book.objects.create(title='A Tale of Two Cities', author='Charles Dickens', publication_year=1859)
        response = self.client.get('/books/?ordering=title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))