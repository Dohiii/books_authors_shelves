"""Serializers for a User API View."""
from django.contrib.auth import (
    get_user_model,
)
from rest_framework import serializers
from rest_framework.response import Response

from profiles.models import Profile


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user object."""

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        user = get_user_model().objects.create_user(**validated_data)
        """Create Profile"""
        Profile.objects.create(
            user=user,
            username=user.name
        )

        return user

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
