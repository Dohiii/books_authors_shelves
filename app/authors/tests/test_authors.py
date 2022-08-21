"""Test for authors APIs."""
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from authors.models import Author
from authors.serializers import AuthorSerializer
from books.models import Book
from tests_helpers import AUTHORS_URL, \
    create_author, \
    create_user, \
    detail_url


class PublicAuthorsApiTests(TestCase):
    """Test UNAUTHORIZED API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_get_not_required(self):
        res = self.client.get(AUTHORS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_auth_post_required(self):
        payload = {
            'name': 'Sample Author',
            'wiki_url': 'Some Urls',
        }
        res = self.client.post(AUTHORS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAuthorsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='pass123')
        self.client.force_authenticate(self.user)

    def test_auth_required(self):
        payload = {
            "name": "Some Name",
            "wiki_url": "https://wikipedia.com/sdf3r3fsd"
        }
        res = self.client.post(AUTHORS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_author_create(self):
        create_author()
        res = self.client.get(AUTHORS_URL)

        recipes = Author.objects.all().order_by('-id')
        serializer = AuthorSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_same_name_not_allowed(self):
        create_author('Mallanga')
        another_author = {
            'name': 'Mallanga'
        }

        res = self.client.post(AUTHORS_URL, another_author)

        self.assertEqual(res.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(res.data["error"], "Author already exist")

    def test_author_update(self):
        create_author()
        res = self.client.get(AUTHORS_URL)

        recipes = Author.objects.all().order_by('-id')
        serializer = AuthorSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_single_author(self):
        author = create_author()
        url = detail_url(author.id)
        res = self.client.get(url)
        serializer = AuthorSerializer(author)

        self.assertEqual(res.data, serializer.data)

    def test_add_book_to_author(self):
        new_author_data = {
            'name': 'Frank Buffalo'
        }
        new_author_data2 = {
            'name': 'Bob Buffalo'
        }
        frank = Author.objects.create(**new_author_data)
        bob = Author.objects.create(**new_author_data2)
        new_book_data = {
            "external_id": "sfas12412",
            "title": "Box And Toys 2",
            "published_year": "2004",
            "acquired": True,
            "thumbnail": ""
        }
        book = Book.objects.create(**new_book_data)
        book.authors.add(frank)
        book.authors.add(bob)

        self.assertEqual(book.authors.count(), 2)

    def test_partial_update_author(self):
        original_link = 'https://pl.wikipedia.org/wiki/J.R.R._Tolkien'
        manakin = create_author('Manakin')

        payload = {'name': 'Mr. Manakin'}
        res = self.client.patch(detail_url(manakin.id), payload)
        # serializer = AuthorSerializer(new_data)

        # self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        manakin.refresh_from_db()
        self.assertEqual(manakin.name, payload['name'])
        self.assertEqual(manakin.wiki_url, original_link)

    def test_author_update_to_existed_name(self):
        author1 = create_author('Author1')
        create_author('Author2')

        payload = {'name': 'Author2'}
        res = self.client.patch(detail_url(author1.id), payload)

        self.assertEqual(res.status_code, status.HTTP_409_CONFLICT)

    def test_unable_to_edit_id(self):
        author1 = create_author('Author1')

        payload = {
            'id': '333fdf',
            'name': 'Author2',
        }

        res = self.client.patch(detail_url(author1.id), payload)

        self.assertEqual(res.data['id'], str(author1.id))
        self.assertNotEqual(res.data['id'], payload['id'])

    def test_full_update(self):
        author = create_author(name='Ford')
        payload = {
            "name": "J J Filips",
            "wiki_url": "http://www.example.com"
            }
        res = self.client.put(detail_url(author.id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        author.refresh_from_db()

    def test_not_valid_url(self):
        payload = {
            'name': 'Tolkien',
            'wiki_url': 'htp:\\wiki_not_a_url..com',
        }

        res = self.client.post(AUTHORS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data, {"wiki_url": ["Enter a valid URL."]})

    def test_delete_author(self):
        author = create_author()
        self.assertEqual(Author.objects.all().count(), 1)
        self.client.delete(detail_url(author.id))
        self.assertEqual(Author.objects.all().count(), 0)


