from rest_framework import serializers
from authors.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    books = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Author
        fields = [
            'id',
            'name',
            'books',
                  ]
        extra_kwargs = {
            'name': {'validators': []},
        }
        depth = 1

    def create(self, validated_data):
        author, created = Author.custom_objects.get_or_create_authors(
                                                        validated_data)
        return author
