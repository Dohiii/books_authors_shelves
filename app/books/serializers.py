from rest_framework import serializers
from books.models import Book
from authors.models import Author
from authors.serializers import AuthorSerializer


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)

    class Meta:
        model = Book
        fields = [
            'id',
            'external_id',
            'title',
            'authors',
            'published_year',
            'pages',
            'acquired',
            'thumbnail'
        ]
        depth = 1

        extra_kwargs = {
            'name': {'validators': []},
        }

    @staticmethod
    def get_or_create_authors(authors):
        author_ids = []
        for author in authors:
            author_instance, created = Author.objects.get_or_create(name=author['name'])
            author_ids.append(author_instance.pk)
        return author_ids

    @staticmethod
    def create_or_update_authors(authors):
        author_ids = []
        for author in authors:
            author_instance, created = Author.objects.update_or_create(name=author['name'])
            author_ids.append(author_instance.pk)
        return author_ids

    def create(self, validated_data):
        authors = validated_data.pop('authors', [])
        book = Book.objects.create(**validated_data)
        book.authors.set(self.get_or_create_authors(authors))
        return book

    def update(self, instance, validated_data):
        author = validated_data.pop('authors', [])
        instance.authors.set(self.create_or_update_authors(author))
        fields = [
            'id',
            'external_id',
            'title',
            'authors',
            'published_year',
            'acquired',
            'thumbnail'
        ]
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except KeyError:  # validated_data may not contain all fields during HTTP PATCH
                pass
        instance.save()
        return instance


