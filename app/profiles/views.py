from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from profiles.models import Profile, ProfileFollowing
from profiles.serializers import ProfileSerializer, \
    ProfileDetailedSerializer
from rest_framework import generics, permissions, status
from django.core.exceptions import ObjectDoesNotExist


class ProfilesListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Profile.objects.all()


class ProfileReadUpdateView(generics.RetrieveUpdateAPIView):
    """View that allows to see only your profile
    no id in url required
    ."""
    serializer_class = ProfileDetailedSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    http_method_names = ['get', 'patch']
    lookup_field = 'uuid'

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return Profile.objects.filter(user=self.request.user).first()

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class FollowProfile(generics.CreateAPIView):
    serializer_class = ProfileSerializer
    queryset = ProfileFollowing.objects.all()
    # serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            to_follow_id = request.data['profile_to_follow']
            to_follow = Profile.objects.get(id=to_follow_id)
        except ValidationError:
            return Response({'invalid': f'This is not a valid ID'},
                            status.HTTP_400_BAD_REQUEST)

        try:
            ProfileFollowing.objects.create(user_id=self.request.user.profile,
                                            following_user_id=to_follow)
            return Response({'success': f'{self.request.user.profile} followed {to_follow}'})
        except IntegrityError:
            return Response({'invalid': f'You already follow {to_follow}'},
                            status.HTTP_400_BAD_REQUEST)

        # followers_of_to_follow_object = to_follow.followers.all()
        #
        # for follower in followers_of_to_follow_object.all():
        #     if follower.user_id.id:
        #         return Response({'invalid': f'You already follow {to_follow}'},
        #                         status.HTTP_400_BAD_REQUEST)


class UnFollowProfile(generics.DestroyAPIView):
    serializer_class = ProfileSerializer
    queryset = ProfileFollowing.objects.all()
    # serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def destroy(self, request, *args, **kwargs):
        try:
            to_unfollow_id = request.data['profile_to_unfollow']
            to_unfollow = Profile.objects.get(id=to_unfollow_id)
        except ValidationError:
            return Response({'invalid': f'This is not a valid ID'},
                            status.HTTP_400_BAD_REQUEST)
        print(to_unfollow)

        try:
            ProfileFollowing.objects.get(user_id=self.request.user.profile,
                                         following_user_id=to_unfollow).delete()
            return Response({'success': f'{self.request.user.profile} unfollowed {to_unfollow}'})
        except ObjectDoesNotExist:
            return Response({'invalid': f'You do not follow {to_unfollow}'},
                            status.HTTP_400_BAD_REQUEST)
