from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from authors.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    books = serializers.StringRelatedField(read_only=True, many=True)
    name = serializers.CharField(max_length=255,
                                 validators=[UniqueValidator(
                                     queryset=Author.objects.all(),
                                     message={
                                         'invalid': 'Author with this '
                                                    'name already exist'
                                     })],
                                 )

    class Meta:
        model = Author
        fields = [
            'id',
            'name',
            "wiki_url",
            'books',
                  ]
        read_only_fields = ['id']

        extra_kwargs = {
            'name': {
                'validators': [],
                },

        }
        depth = 1

    #
    def update(self, instance, validated_data):
        fields = [
            'name',
            "wiki_url",
        ]
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            # validated_data may not contain all fields during HTTP PATCH
            except KeyError:
                pass
        instance.save()
        return instance
