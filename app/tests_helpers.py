from django.contrib.auth import get_user_model
from django.urls import reverse

from authors.models import Author
from books.models import Book
from profiles.models import Profile

AUTHORS_URL = reverse('authors:author-list')
BOOKS_URL = reverse('books:book-list')
IMPORT_URL = '/api/v1/import_author/'
IMPORT_BOOKS_URL = '/api/v1/import_book/'
SHELVES_PUBLIC_URL = '/api/v1/shelves_public/'
SHELVES_URL = '/api/v1/shelves/'
PROFILES_URL = '/api/v1/profiles/'
PROFILE_URL = '/api/v1/profile/'


def author_detail_url(obj_id):
    """Create and return an author detail URL."""
    return reverse('authors:author-detail', args=[obj_id])


def book_detail_url(obj_id):
    """Create and return a book detail URL."""
    return reverse('books:book-detail', args=[obj_id])


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


def create_profile(user, **params):
    profile = Profile.objects.create(user=user, **params)
    return profile


def create_author(user, name='Mark Twain',
                  wiki_url='https://pl.wikipedia.org/wiki/J.R.R._Tolkien'):
    """Create and return a sample author."""
    defaults = {
        'user': user,
        'name': name,
        'wiki_url': wiki_url,
    }

    author = Author.objects.create(**defaults)
    return author


def create_book(user, **kwargs):
    """Create and return a sample author."""
    defaults = {
        'user': user,
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
