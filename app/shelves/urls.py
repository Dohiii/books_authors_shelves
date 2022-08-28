"""
URL mappings for a shelf API.
"""
from django.urls import (
    path,
    include,
)

from shelves.views import ShelfViewSet, ListPublicShelves, ShelfAddBook
from rest_framework.routers import DefaultRouter


app_name = 'shelf'


router = DefaultRouter()
router.register('shelves', ShelfViewSet)
router.register('shelves/shelf_add', ShelfAddBook)

urlpatterns = [
    path('shelves_public/', ListPublicShelves.as_view(), name='shelves_public'),
    path('', include(router.urls)),
]



