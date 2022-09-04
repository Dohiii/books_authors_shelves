"""Test for recipe APIs."""
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase

from books.models import Book
from tests_helpers import (
    create_user,
    create_profile,
    create_book,
    create_shelf
)
from rest_framework import status


class PublicBooksApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='pass123')
        self.profile = create_profile(user=self.user, username='Val')
        self.book = create_book(user=self.profile, title="Book2",
                                external_id="7L_ra-0NDvMC")
        self.client.force_authenticate(self.user)

    def test_create_shelf(self):
        """Test shelf creation"""
        url = '/api/v1/shelves/'
        payload = {
            "shelf_name": "Shelf It is ",
            "description": "What is this?",
            "access": "PUBLIC"
        }

        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_add_books_to_shelf(self):
        """Test add books to shelf"""
        shelf = create_shelf(user=self.profile)

        url = f'/api/v1/shelves/shelf_add/{shelf.id}/'
        payload = {
            "books": [{"external_id": f"{self.book.external_id}"}]}
        res = self.client.patch(url, payload)

        self.assertTrue(res.status_code, status.HTTP_200_OK)
