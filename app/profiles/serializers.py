from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from profiles.models import Profile, ProfileFollowing
from shelves.models import Shelf


class FollowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileFollowing
        fields = ["following_user_id", "created"]


class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileFollowing
        fields = ["user_id", "created"]


class ProfileSerializer(serializers.ModelSerializer):
    added_books = serializers.IntegerField(
                                            source='added_books.count',
                                            read_only=True
                                            )
    added_authors = serializers.IntegerField(
                                            source='added_authors.count',
                                            read_only=True
                                            )

    following = serializers.IntegerField(
                                            source='following.count',
                                            read_only=True
                                            )
    followers = serializers.IntegerField(
                                            source='followers.count',
                                            read_only=True
                                            )


    """Nice Looking serializer of following object. Need to add that to details only serializer"""
    # following = serializers.SerializerMethodField()
    # followers = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'username',
            'created_at',
            'added_books',
            'added_authors',
            'followers',
            'following',

        ]
        read_only_fields = [
            'id',
            'user',
            'added_books',
            'added_authors',
            'followers',
            'following',


        ]
        extra_kwargs = {
            'name': {'validators': []},
        }

    def create(self, validated_data):

        return Profile.objects.create(**validated_data)

    def get_following(self, obj):
        return FollowingSerializer(obj.following.all(), many=True).data

    def get_followers(self, obj):
        return FollowersSerializer(obj.followers.all(), many=True).data


class ProfileDetailedSerializer(serializers.ModelSerializer):
    added_books = serializers.IntegerField(
                                            source='added_books.count',
                                            read_only=True
                                            )
    added_authors = serializers.IntegerField(
                                            source='added_authors.count',
                                            read_only=True
                                            )

    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'username',
            'created_at',
            'added_books',
            'added_authors',
            'followers',
            'following',

        ]
        read_only_fields = [
            'id',
            'user',
            'added_books',
            'added_authors',
            'followers',
            'following',


        ]
        extra_kwargs = {
            'name': {'validators': []},
        }

    # def create(self, validated_data):
    #     return Profile.objects.create(**validated_data)

    def get_following(self, obj):
        return FollowingSerializer(obj.following.all(), many=True).data

    def get_followers(self, obj):
        return FollowersSerializer(obj.followers.all(), many=True).data
