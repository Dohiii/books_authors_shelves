import uuid
from django.db import models
from profiles.models import Profile


class AuthorModel(models.Manager):
    @staticmethod
    def is_author_exist(name):
        return Author.objects.filter(name=name).exists()


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='added_authors'
    )
    name = models.CharField(max_length=255)
    wiki_url = models.URLField(max_length=500, null=True)
    objects = models.Manager()
    custom_objects = AuthorModel()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
