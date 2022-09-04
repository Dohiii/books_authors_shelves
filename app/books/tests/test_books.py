"""Test for recipe APIs."""
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from books.models import Book
from books.serializers import BookSerializer
from profiles.models import Profile
from tests_helpers import BOOKS_URL,\
    book_detail_url, \
    create_user, \
    create_book, \
    create_author, \
    create_profile


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
        self.user = create_user(email='user@example.com',
                                password='pass123')
        self.profile = create_profile(user=self.user, username='Val')
        self.client.force_authenticate(self.user)

    def test_auth_post_book(self):
        create_book(user=self.profile)
        res = self.client.get(BOOKS_URL)

        book = Book.objects.all().order_by('-id')
        serializer = BookSerializer(book, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_add_authors(self):
        author1 = create_author(user=self.profile, name='Tolkien')
        author2 = create_author(user=self.profile, name='Jerm K Jerome')
        res = self.client.get(BOOKS_URL)
        book = Book.objects.all().order_by('-id')

        book.__setattr__('authors', [])
        book.authors.append(author1)
        book.authors.append(author2)

        serializer = BookSerializer(book, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(book.authors), 2)

    def test_retrieve_books(self):
        """Test Get ALL books"""
        create_book(user=self.profile)
        create_book(user=self.profile, external_id='asf2442')

        res = self.client.get(BOOKS_URL)

        books = Book.objects.all().order_by('published_year')
        serializer = BookSerializer(books, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_books_limited_to_user(self):
        """Test Get ALL books"""
        other_user = create_user(email='other@example.com',
                                 password='pass123')
        other_profile = create_profile(user=other_user,
                                       username='Babum')

        create_book(user=self.profile)
        create_book(user=self.profile, external_id='assf442')
        create_book(user=other_profile, external_id='asf2442')

        res = self.client.get(BOOKS_URL)

        books = Book.objects.filter(user=self.profile)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(books.count(), 2)

    def test_get_single_book(self):
        book = create_book(user=self.user.profile)
        url = book_detail_url(book.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], 'Box And Toys 2')

    def test_delete_book(self):
        book = create_book(user=self.user.profile)
        self.assertEqual(Book.objects.all().count(), 1)
        self.client.delete(book_detail_url(book.id))
        self.assertEqual(Book.objects.all().count(), 0)

    def test_delete_book_you_owned(self):
        book1 = create_book(user=self.user.profile,
                            external_id='saf23ff')
        user2 = create_user(email='user2@example.com',
                            password='pass123')
        profile2 = Profile.objects.create(user=user2,
                                          username='Mommy')
        book2 = create_book(user=profile2,
                            external_id='safa3224')

        """ Try to delete not the author you created(Invalid)"""
        url = book_detail_url(book2.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data, {"invalid":
                                    "You can delete only your items"})

        """ Try to delete the author you created(Success)"""
        url2 = book_detail_url(book1.id)

        res = self.client.delete(url2)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(res.data, {'success': 'Item was deleted'})
