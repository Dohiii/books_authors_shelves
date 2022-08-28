"""
Views for the user API.
"""
from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user
