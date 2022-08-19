"""
URL mappings for the author app.
"""
from django.urls import (
    path,
    include,
    re_path,
)
from authors.views import ImportAuthor, AuthorViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('authors', AuthorViewSet)

app_name = "authors"

urlpatterns = [
    path('', include(router.urls)),
    re_path('import_author/',
            ImportAuthor.as_view(), name='import_author')
]
