"""Test for authors APIs."""
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from authors.models import Author
from authors.serializers import AuthorSerializer
from books.models import Book
from profiles.models import Profile
from tests_helpers import AUTHORS_URL, \
    create_author, \
    create_user, \
    author_detail_url


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
        Profile.objects.create(user=self.user, username='Dohiii')
        self.client.force_authenticate(self.user)

    def test_auth_required(self):
        payload = {
            "user": self.user.profile,
            "name": "Some Name",
            "wiki_url": "https://wikipedia.com/sdf3r3fsd"
        }
        res = self.client.post(AUTHORS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_author_create(self):
        create_author(self.user.profile)
        res = self.client.get(AUTHORS_URL)

        authors = Author.objects.all().order_by('-id')
        serializer = AuthorSerializer(authors, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_same_name_not_allowed(self):
        create_author(user=self.user.profile, name='Mallanga')
        another_author = {
            'user': self.user.profile,
            'name': 'Mallanga'
        }

        res = self.client.post(AUTHORS_URL, another_author)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['name'],
                         {"invalid": "Author with this name already exist"})

    def test_author_update(self):
        create_author(self.user.profile)
        res = self.client.get(AUTHORS_URL)

        authors = Author.objects.all().order_by('-id')
        serializer = AuthorSerializer(authors, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_single_author(self):
        author = create_author(user=self.user.profile)
        url = author_detail_url(author.id)
        res = self.client.get(url)
        serializer = AuthorSerializer(author)

        self.assertEqual(res.data, serializer.data)

    def test_add_book_to_author(self):
        new_author_data = {
            'user': self.user.profile,
            'name': 'Frank Buffalo'
        }
        new_author_data2 = {
            'user': self.user.profile,
            'name': 'Bob Buffalo'
        }
        frank = Author.objects.create(**new_author_data)
        bob = Author.objects.create(**new_author_data2)
        new_book_data = {
            'user': self.user.profile,
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
        manakin = create_author(user=self.user.profile, name='Manakin')

        payload = {'name': 'Mr. Manakin'}
        res = self.client.patch(author_detail_url(manakin.id), payload)
        # serializer = AuthorSerializer(new_data)

        # self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        manakin.refresh_from_db()
        self.assertEqual(manakin.name, payload['name'])
        self.assertEqual(manakin.wiki_url, original_link)

    def test_author_update_to_existed_name(self):
        author1 = create_author(user=self.user.profile, name='Author1')
        create_author(user=self.user.profile, name='Author2')

        payload = {'name': 'Author2'}
        res = self.client.patch(author_detail_url(author1.id), payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unable_to_edit_id(self):
        author1 = create_author(user=self.user.profile, name='Author1')

        payload = {
            'id': '333fdf',
            'name': 'Author2',
        }

        res = self.client.patch(author_detail_url(author1.id), payload)

        self.assertEqual(res.data['id'], str(author1.id))
        self.assertNotEqual(res.data['id'], payload['id'])

    def test_full_update(self):
        author = create_author(user=self.user.profile, name='Ford')
        payload = {
            "name": "J J Filips",
            "wiki_url": "http://www.example.com"
            }
        res = self.client.put(author_detail_url(author.id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        author.refresh_from_db()

    def test_not_valid_url(self):
        payload = {
            'user': self.user.profile,
            'name': 'Tolkien',
            'wiki_url': 'htp:\\wiki_not_a_url..com',
        }

        res = self.client.post(AUTHORS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data, {"wiki_url": ["Enter a valid URL."]})

    def test_delete_author(self):
        author = create_author(user=self.user.profile, name='Ford')
        self.assertEqual(Author.objects.all().count(), 1)
        self.client.delete(author_detail_url(author.id))
        self.assertEqual(Author.objects.all().count(), 0)

    def test_delete_author_you_owned(self):
        author1 = create_author(user=self.user.profile, name='Ford')
        user2 = create_user(email='user2@example.com', password='pass123')
        profile2 = Profile.objects.create(user=user2, username='Mommy')
        author2 = create_author(user=profile2, name='Author1')

        """ Try to delete not the author you created(Invalid)"""
        url = author_detail_url(author2.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data, {"invalid":
                                    "You can delete only your items"})

        """ Try to delete the author you created(Success)"""
        url2 = author_detail_url(author1.id)

        res = self.client.delete(url2)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(res.data, {'success': 'Item was deleted'})
