"""
URL mappings for a shelf API.
"""
from django.urls import (
    path,
    include,
)

from shelves.views import (
    ShelfViewSet,
    ListPublicShelves,
    ShelfAddBook,
    GetShelfOfFriend
)
from rest_framework.routers import DefaultRouter


app_name = 'shelf'


router = DefaultRouter()
router.register('shelves', ShelfViewSet)
router.register('shelves/shelf_add', ShelfAddBook)

urlpatterns = [
    path('shelves/public/', ListPublicShelves.as_view(),
         name='shelves_public'),
    path('shelf_of_friend/', GetShelfOfFriend.as_view(),
         name='shelf_of_friend'),
    path('', include(router.urls)),
]
