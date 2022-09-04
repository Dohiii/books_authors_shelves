"""Test for authors import APIs."""
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from tests_helpers import IMPORT_URL
from tests_helpers import create_user, create_profile


class ImportAuthorsPublic(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_import_need_auth(self):
        with self.assertRaises(AttributeError):
            payload = {
                "name": "Tolkien"
            }
            self.client.put(IMPORT_URL, payload)


class ImportAuthorsPrivate(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com',
                                password='pass123')
        self.profile = create_profile(user=self.user, username='Val')
        self.client.force_authenticate(self.user)

    def test_import_author_get_not_allowed(self):
        res = self.client.get(IMPORT_URL)
        self.assertEqual(res.data["detail"], "Method \"GET\" not allowed.")

    def test_put_successful(self):
        payload = {
            "user": self.profile,
            "name": "Tolkien"
        }

        res = self.client.put(IMPORT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # test wiki import works and add wiki_url
        self.assertIsNotNone(res.data['wiki_url'])
        # test wiki import works and add Wiki title
        self.assertNotEqual(res.data['name'], payload['name'])

    def test_same_name_not_allowed(self):
        first_author = {
            'user': self.profile,
            'name': 'Tolkien'
        }

        another_author = {
            'user': self.profile,
            'name': 'Tolkien'
        }

        res = self.client.put(IMPORT_URL, first_author)
        res2 = self.client.put(IMPORT_URL, another_author)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res2.data['name'],
                         {"invalid": "Author with this name already exist"})
