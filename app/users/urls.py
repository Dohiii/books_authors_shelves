"""
URL mappings for a user API.
"""
from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register_user'),
    path('user_me/', views.ManageUserView.as_view(), name='user_me'),
]
