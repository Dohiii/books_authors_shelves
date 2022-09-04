import uuid
from django.db import models
from books.models import Book
from profiles.models import Profile


class Shelf(models.Model):
    ACCESS_CHOICES = (
        ("PRIVATE", "PRIVATE"),
        ("PUBLIC", "PUBLIC"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE,
                             related_name='shelves')
    shelf_name = models.CharField(max_length=255, null=True,
                                  default='Shelf')
    description = models.TextField(blank=True)

    books = models.ManyToManyField(Book, related_name='books',
                                   blank=True)
    access = models.CharField(max_length=7, choices=ACCESS_CHOICES,
                              default='PRIVATE')

    # date and time data
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.shelf_name
