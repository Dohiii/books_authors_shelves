"""Test for recipe APIs."""
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from tests_helpers import IMPORT_BOOKS_URL, \
    create_user, \
    create_profile


class PublicBooksImportTests(TestCase):
    """Test UNAUTHORIZED API requests."""
    def setUp(self):
        self.client = APIClient()

    def test_auth_get_not_required(self):
        res = self.client.get(IMPORT_BOOKS_URL)

        self.assertEqual(res.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_auth_post_required(self):
        payload = {
            'name': 'Tolkien'
        }
        res = self.client.post(IMPORT_BOOKS_URL, payload)

        self.assertEqual(res.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)


class PrivateBooksImportTests(TestCase):
    """Test Authorised API requests"""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com',
                                password='pass123')
        self.profile = create_profile(user=self.user,
                                      username='Val')
        self.client.force_authenticate(self.user)

    def test_no_post_allowed(self):
        payload = {
            'name': 'Tolkien'
        }
        res = self.client.post(IMPORT_BOOKS_URL, payload)
        self.assertEqual(res.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_no_author_exist_error(self):
        payload = {
            'name': 'asf fasf fd'
        }
        res = self.client.put(IMPORT_BOOKS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['invalid'],
                         'Author with this name does not exist')

    def test_unexpected_input(self):
        payload = {
            'name': 22,
            'wiki_url': True
        }
        res = self.client.put(IMPORT_BOOKS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['invalid'],
                         'Author with this name does not exist')

    def test_put_success(self):
        payload = {
            'user': self.user,
            'name': 'Tolkien'
        }
        res = self.client.put(IMPORT_BOOKS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['imported'], 10)
