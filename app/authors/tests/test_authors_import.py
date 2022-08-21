"""Test for authors import APIs."""
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from authors.models import Author
from authors.serializers import AuthorSerializer
from books.models import Book
from tests_helpers import IMPORT_URL
from tests_helpers import AUTHORS_URL, \
    create_author, \
    create_user, \
    detail_url


class ImportAuthorsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='pass123')
        self.client.force_authenticate(self.user)

    def test_import_author_get_not_allowed(self):
        res = self.client.get(IMPORT_URL)

        self.assertEqual(res.data["detail"], "Method \"GET\" not allowed.")

