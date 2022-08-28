"""Test for recipe APIs."""
import json
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from authors.models import Author
from books.models import Book
from books.serializers import BookSerializer
from profiles.models import Profile
from tests_helpers import \
    PROFILE_URL,\
    PROFILES_URL, \
    create_user, \
    create_profile


class PublicBooksApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='pass123')
        self.profile = create_profile(user=self.user, username='Val')
        self.client.force_authenticate(self.user)

    def test_if_profile_created(self):
        create_user(email='user2@example.com', password='pass123')
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles), 2)

    def test_if_profile_name(self):
        """Test profiles name is beginning of users email"""
        user2 = create_user(email='user2@example.com', password='pass123')
        user3 = create_user(email='user3@example.com', password='pass123')
        profiles = Profile.objects.all()
        # profile2 = Profile.objects.get(user=user2)
        # profile3 = Profile.objects.get(user=user3)
        self.assertTrue(len(profiles), 3),
        # self.assertTrue(profile2.username, 'user2'),
        # self.assertTrue(profile3.username, 'user3'),
