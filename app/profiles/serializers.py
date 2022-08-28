from rest_framework import serializers
from profiles.models import Profile
from shelves.models import Shelf


class ProfileSerializer(serializers.ModelSerializer):
    added_books = serializers.IntegerField(
                                            source='added_books.count',
                                            read_only=True
                                            )
    added_authors = serializers.IntegerField(
                                            source='added_authors.count',
                                            read_only=True
                                            )

    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'username',
            'created_at',
            'added_books',
            'added_authors',

        ]
        read_only_fields = [
            'id',
            'user',
            'added_books',
            'added_authors',


        ]
        extra_kwargs = {
            'name': {'validators': []},
        }

    def create(self, validated_data):

        return Profile.objects.create(**validated_data)
