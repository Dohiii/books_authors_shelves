from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from books.serializers import BookSerializer
from books.models import Book
from shelves.models import Shelf


class ShelfAddBookSerializer(serializers.ModelSerializer):
    """Separate serializer for adding book to a bookshelf"""
    books = BookSerializer(many=True)

    class Meta:
        model = Shelf
        fields = [
            'id',
            'user',
            'shelf_name',
            'description',
            'access',
            "books",
            "created_at",
            "updated_at",

        ]
        # read_only_fields = [
        #     'id',
        #     'user',
        #     "created_at",
        #     "updated_at",
        # ]
        extra_kwargs = {
            'name': {'validators': []},
        }

    def update(self, instance, validated_data):
        # print(dir(validated_data))
        # print(len(validated_data['books'][0].items()))

        books_data = validated_data.pop('books', [])
        print(books_data)
        books_list = []

        existing_books = instance.books.all()

        for book in existing_books:
            books_list.append(book)

        for book in books_data:
            try:
                obj = Book.objects.get(external_id=book['external_id'])
                books_list.append(obj)

            except KeyError:
                print('Oh no')

        instance.books.set(books_list)
        fields = [
            'shelf_name',
            'description',
            'access',
            'books',
        ]

        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            # validated_data may not contain all fields during HTTP PATCH
            except KeyError:
                pass
        instance.save()
        return instance


class ShelfSerializer(serializers.ModelSerializer):
    """Main serializer for Shelf logic"""
    books_count = serializers.IntegerField(
        source='books.count',
        read_only=True
    )

    shelf_name = serializers.CharField(
        max_length=255,
        validators=[UniqueValidator(
                    queryset=Shelf.objects.all(),
                    message={
                            'invalid': 'Shelf with this title already exist'
                             }
                    )],)

    class Meta:
        model = Shelf
        fields = [
            'id',
            'user',
            'shelf_name',
            'description',
            'books_count',
            'access',
            "created_at",
            "updated_at",
            # 'url'

        ]
        read_only_fields = [
            'id',
            'user',
            'books_count',
            'books',
        ]
        extra_kwargs = {
            'name': {'validators': []},
        }

    def create(self, validated_data):
        return Shelf.objects.create(**validated_data)
