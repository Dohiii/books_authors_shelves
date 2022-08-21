from django.test import TestCase
from django.contrib.auth import get_user_model
from authors.models import Author
from tests_helpers import (
    create_author,
    create_user,
    create_book
    )


class AuthorModelTests(TestCase):
    def test_create_author(self):
        """Test creating a recipe is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'password123',
        )
        author = Author.objects.create(
            name='Author of the Book',
            wiki_url='https://wiki.com/author_of_the_book'
        )

        self.assertEqual(str(author), author.name)

    def test_is_author_exist(self):
        create_author('Tolkien')

        self.assertTrue(Author.custom_objects.is_author_exist('Tolkien'))
        self.assertFalse(Author.custom_objects.is_author_exist('Mark Twain'))

    def return_str(self):
        create_author('Tolkien')
        author = Author.objects.filter(name='Tolkien').first()
        self.assertEqual(author.name, author.__str__())

