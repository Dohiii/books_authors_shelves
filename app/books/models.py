import uuid
from django.db import models
from authors.models import Author



class Producto:
    pass


class Book(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4, editable=False)
    external_id = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255, null=True, default='Book')
    authors = models.ManyToManyField(Author, related_name='books',
                                     blank=True, unique=False,
                                     default=None,
                                     )
    published_year = models.CharField(max_length=255, blank=True,
                                      null=True)
    pages = models.IntegerField(blank=True, null=True)
    acquired = models.BooleanField(default=True)
    thumbnail = models.TextField(blank=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title
