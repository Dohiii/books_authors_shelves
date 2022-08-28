from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework import serializers
from books.models import Book
from authors.models import Author
from authors.serializers import AuthorSerializer


class BookListSerializer(serializers.ModelSerializer):
    authors = serializers.StringRelatedField(read_only=True, many=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Book
        fields = [
            'id',
            'user',
            'external_id',
            'title',
            'authors',
            'published_year',
            'pages',
            'acquired',
            'thumbnail'
        ]


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Book
        fields = [
            'id',
            'user',
            'external_id',
            'title',
            'authors',
            'published_year',
            'pages',
            'acquired',
            'thumbnail'
        ]
        depth = 1

        # read_only_fields = ['id', 'user']

        extra_kwargs = {
            'name': {'validators': []},
            'external_id': {
                'validators': []},
        }

    def create(self, validated_data):
        print('Serializer Created')
        authors_data = validated_data.pop('authors')
        book = Book.objects.create(**validated_data)

        auth_list = []

        for author in authors_data:
            auth_list.append(Author.objects.create(user=book.user, **author))

        book.authors.set(auth_list)

        return book

    def update(self, instance, validated_data):
        print('Serializer Updated')
        authors = validated_data.pop('authors', [])
        print(authors)
        auth_list = []
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        for author in authors:
            try:
                obj = Author.objects.get(name=author)
                obj.name = validated_data['name']
                obj.wiki_url = validated_data['wiki_url']
            except ObjectDoesNotExist:
                auth_list.append(Author.objects.create(user=user.profile, **author))
        instance.authors.set(auth_list)
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
            # validated_data may not contain all fields during HTTP PATCH
            except KeyError:
                pass
        instance.save()
        return instance
