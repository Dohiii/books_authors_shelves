"""
URL mappings for a user API.
"""
from django.urls import path
from profiles.views import ProfileViewReadUpdate

app_name = 'profile'

urlpatterns = [
    path('profile/', ProfileViewReadUpdate.as_view(), name='profile'),
]
