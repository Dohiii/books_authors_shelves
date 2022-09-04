"""Test for recipe APIs."""
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from profiles.models import Profile
from tests_helpers import (
    PROFILE_URL,
    create_user,
    create_profile)


class PublicBooksApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='pass123')
        self.profile = create_profile(user=self.user, username='Val')
        self.user2 = create_user(email='user2@example.com', password='pass123')
        self.profile2 = create_profile(user=self.user2, username='Doh')
        self.user3 = create_user(email='user4@example.com', password='pass123')
        self.profile3 = create_profile(user=self.user3, username='Mog')

        self.client.force_authenticate(self.user3)

        payload = {
            "profile_to_follow": self.profile2.id
        }
        self.client.post('/api/v1/profiles/follow/', payload)

        self.client.force_authenticate(self.user)

    def test_if_profile_created(self):
        """Test profile creation"""
        create_user(email='user3@example.com', password='pass123')
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles), 2)

    def test_partial_update_author(self):
        """Test successful partial update of profile"""
        payload = {'username': 'Mr. Manakin'}
        res = self.client.patch(f'{PROFILE_URL}', payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.username, payload['username'])

    def test_follow_profile(self):
        """Test successful user following"""
        self.assertEqual(self.profile.following.all().count(), 0)
        self.assertEqual(self.profile2.followers.all().count(), 1)
        payload = {
                    "profile_to_follow": self.profile2.id
                    }
        res = self.client.post('/api/v1/profiles/follow/', payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.profile.following.all().count(), 1)
        self.assertEqual(self.profile2.followers.all().count(), 2)

    def test_follow_wrong_id(self):
        """Test follow user fails with not existed ID input"""
        self.assertEqual(self.profile.following.all().count(), 0)
        self.assertEqual(self.profile2.followers.all().count(), 1)
        payload = {
            "profile_to_follow": "WRONG ID"
        }
        res = self.client.post('/api/v1/profiles/follow/', payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['invalid'], 'This is not a valid ID')
        self.assertEqual(self.profile.following.all().count(), 0)

    def test_follow_same_user(self):
        """Test follow user fails with not existed ID input"""
        self.client.force_authenticate(self.user3)
        self.assertEqual(self.profile3.following.all().count(), 1)
        payload = {
            "profile_to_follow": self.profile2.id
        }
        res = self.client.post('/api/v1/profiles/follow/', payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['invalid'],
                         f'You already follow {self.profile2}')

    def test_unfollow_profile(self):
        """Test successful unfollow user"""
        payload_follow = {
            "profile_to_follow": self.profile2.id
        }
        res = self.client.post('/api/v1/profiles/follow/', payload_follow)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.profile.following.all().count(), 1)
        self.assertEqual(self.profile2.followers.all().count(), 2)

        payload_unfollow = {
            "profile_to_unfollow": self.profile2.id
        }

        res_unfollow = self.client.delete('/api/v1/profiles/unfollow/',
                                          payload_unfollow)

        self.assertEqual(res_unfollow.status_code, status.HTTP_200_OK)
        self.assertEqual(self.profile.following.all().count(), 0)
        self.assertEqual(self.profile2.followers.all().count(), 1)

    def test_unable_to_unfollow_if_not_followed(self):
        """Test unable unfollow profile if you are not following it"""
        payload_follow = {
            "profile_to_follow": self.profile2.id
        }
        res = self.client.post('/api/v1/profiles/follow/', payload_follow)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.profile.following.all().count(), 1)
        self.assertEqual(self.profile2.followers.all().count(), 2)

        payload_unfollow = {
            "profile_to_unfollow": self.profile3.id
        }

        res_unfollow = self.client.delete('/api/v1/profiles/unfollow/',
                                          payload_unfollow)

        self.assertEqual(res_unfollow.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(res.data['invalid'],
        #                  f'You do not follow {self.profile3}')
