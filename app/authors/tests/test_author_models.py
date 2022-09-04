from django.test import TestCase
from django.contrib.auth import get_user_model
from authors.models import Author
from profiles.models import Profile
from tests_helpers import (
    create_author,
    )


class AuthorModelTests(TestCase):
    def test_create_author(self):
        """Test creating a recipe is successful."""
        self.user = get_user_model().objects.create_user(
            'test@example.com',
            'password123',
        )
        Profile.objects.create(user=self.user, username='Dohiii')
        author = Author.objects.create(
            user=self.user.profile,
            name='Author of the Book',
            wiki_url='https://wiki.com/author_of_the_book'
        )

        self.assertEqual(str(author), author.name)

    def test_is_author_exist(self):
        self.user = get_user_model().objects.create_user(
            'test@example.com',
            'password123',
        )
        Profile.objects.create(user=self.user, username='Dohiii')
        create_author(user=self.user.profile, name='Tolkien')

        self.assertTrue(Author.custom_objects.is_author_exist('Tolkien'))
        self.assertFalse(Author.custom_objects.is_author_exist('Mark Twain'))

    def return_str(self):
        create_author(user=self.user.profile, name='Tolkien')
        author = Author.objects.filter(name='Tolkien').first()
        self.assertEqual(author.name, author.__str__())
