from rest_framework_simplejwt.authentication import JWTAuthentication
from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from rest_framework import viewsets, generics, permissions


class ProfilesListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Profile.objects.all()


class ProfileReadUpdateView(generics.RetrieveUpdateAPIView):
    """View that allows to see only your profile
    no id in url required
    ."""
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    http_method_names = ['get', 'patch']
    lookup_field = 'uuid'

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return Profile.objects.filter(user=self.request.user).first()

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
