import uuid
from django.db import models
from authors.models import Author
from profiles.models import Profile


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE,
                             related_name='added_books')
    external_id = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255, null=True, default='Book')
    authors = models.ManyToManyField(Author, related_name='books',
                                     blank=True
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
