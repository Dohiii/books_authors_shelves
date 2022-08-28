import uuid
from django.db import models
from profiles.models import Profile


class AuthorModel(models.Manager):
    @staticmethod
    def is_author_exist(name):
        return Author.objects.filter(name=name).exists()

    # @staticmethod
    # def get_or_create_authors(data):
    #     author_instance, created = Author.objects.get_or_create(name=data['name'], user=data['user'])
    #     return author_instance, created
    #
    # @staticmethod
    # def create_or_update_authors(authors):
    #     author_ids = []
    #     for author in authors:
    #         author_instance, created = Author.objects.update_or_create(
    #                                                 name=author['name'])
    #         author_ids.append(author_instance.pk)
    #     return author_ids


class Author(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4, editable=False)
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

