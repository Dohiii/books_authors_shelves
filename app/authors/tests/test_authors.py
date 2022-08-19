"""Test for recipe APIs."""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from authors.models import Author


AUTHORS_URL = reverse('authors:author-list')


def detail_url(author_id):
    """Create and return a recipe detail URL."""
    return reverse('author:author-detail', args=[author_id])


def create_author(**kwargs):
    """Create and return a sample author."""
    defaults = {
        'name': 'J R R Tolkien',
        'wiki_url': 'https://pl.wikipedia.org/wiki/J.R.R._Tolkien'
    }
    defaults.update(kwargs)

    author = Author.objects.create(**defaults)
    return author


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


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
            'name': 'Tolkien',
            'wiki_url': 'Some Urls',
        }
        res = self.client.post(AUTHORS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

