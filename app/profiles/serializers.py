from rest_framework import serializers
from profiles.models import Profile, ProfileFollowing


class FollowingSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField("get_username")

    class Meta:
        model = ProfileFollowing
        fields = [
            "username",
            "following_user_id",
            "created",
        ]

    @staticmethod
    def get_username(obj):
        return obj.following_user_id.username


class FollowersSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField("get_username")

    class Meta:
        model = ProfileFollowing
        fields = [
            "username",
            "user_id",
            "created",
        ]

    @staticmethod
    def get_username(obj):
        return obj.user_id.username


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

    """
    Nice Looking serializer of following object.
    Need to add that to details only serializer
    """
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

    @staticmethod
    def get_following(obj):
        return FollowingSerializer(obj.following.all(), many=True).data

    @staticmethod
    def get_followers(obj):
        return FollowersSerializer(obj.followers.all(), many=True).data
