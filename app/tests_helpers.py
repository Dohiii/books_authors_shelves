from django.contrib.auth import get_user_model
from django.urls import reverse

from authors.models import Author
from books.models import Book

AUTHORS_URL = reverse('authors:author-list')
BOOKS_URL = reverse('books:book-list')
IMPORT_URL = '/api/v1/import_author/'


def detail_url(author_id):
    """Create and return a recipe detail URL."""
    return reverse('authors:author-detail', args=[author_id])


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


def create_author(name='Mark Twain',
                  wiki_url='https://pl.wikipedia.org/wiki/J.R.R._Tolkien'):
    """Create and return a sample author."""
    defaults = {
        'name': name,
        'wiki_url': wiki_url,
    }

    author = Author.objects.create(**defaults)
    return author


def create_book(**kwargs):
    """Create and return a sample author."""
    defaults = {
        "external_id": "sfas12412",
        "title": "Box And Toys 2",
        "published_year": "2004",
        # "authors": None,
        "acquired": True,
        "thumbnail": ""
    }
    defaults.update(kwargs)
    book = Book.objects.create(**defaults)

    return book
