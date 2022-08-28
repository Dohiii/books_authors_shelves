"""
URL mappings for a user API.
"""
from django.urls import path, include
from profiles.views import (
    ProfileReadUpdateView,
    ProfilesListView,
    FollowProfile,
    UnFollowProfile,
    )


app_name = 'profile'

urlpatterns = [
    path('profile/', ProfileReadUpdateView.as_view(), name='profile'),
    path('profiles/', ProfilesListView.as_view(), name='profile-list'),
    path('profiles/follow/', FollowProfile.as_view(), name='profile-follow'),
    path('profiles/unfollow/', UnFollowProfile.as_view(), name='profile-unfollow'),
]
