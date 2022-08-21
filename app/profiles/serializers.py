from rest_framework import serializers
from profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    # books = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Profile
        fields = [
            'id',
            'username',
            'created_at',
            'updated_at',
            'user',
        ]
        extra_kwargs = {
            'name': {'validators': []},
        }

    def create(self, validated_data):
        return Profile.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     fields = [
    #         'name',
    #         "wiki_url",
    #     ]
    #     for field in fields:
    #         try:
    #             setattr(instance, field, validated_data[field])
    #         # validated_data may not contain all fields during HTTP PATCH
    #         except KeyError:
    #             pass
    #     instance.save()
    #     return instance






