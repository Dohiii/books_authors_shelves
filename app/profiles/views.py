from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from profiles.models import Profile
from profiles.serializers import ProfileSerializer
# Create your views here.
from rest_framework import viewsets, generics, permissions


class ProfileViewReadUpdate(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'username'

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return Profile.objects.filter(user=self.request.user).first()

    # def update(self, request, *args, **kwargs):
    #     profile = Profile.objects.filter(user=self.request.user).first()
    #     serializer =


