"""Test for recipe APIs."""
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from books.models import Book
from books.serializers import BookSerializer
from tests_helpers import BOOKS_URL, create_user, create_book, create_author


class PublicBooksApiTests(TestCase):
    """Test UNAUTHORIZED API requests."""
    def setUp(self):
        self.client = APIClient()

    def test_auth_get_not_required(self):
        res = self.client.get(BOOKS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_auth_post_required(self):
        payload = {
            'title': 'Money and Honey',
            'external_id': '12hf2hf',
            'published_year': '2004',
            'pages': 304,
            'acquired': True,
            'thumbnail': 'https://books.com/12hf2hf'
        }
        res = self.client.post(BOOKS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBooksTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='pass123')
        self.client.force_authenticate(self.user)

    def test_auth_post_book(self):
        create_book()
        res = self.client.get(BOOKS_URL)

        book = Book.objects.all().order_by('-id')
        serializer = BookSerializer(book, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_add_authors(self):
        author1 = create_author('Tolkien')
        author2 = create_author('Jerm K Jerome')
        res = self.client.get(BOOKS_URL)
        book = Book.objects.all().order_by('-id')
        # authors = Book.objects.all().order_by('-id')

        book.__setattr__('authors', [])
        book.authors.append(author1)
        book.authors.append(author2)

        serializer = BookSerializer(book, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(book.authors), 2)





