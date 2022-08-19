"""
URL mappings for the author app.
"""
from django.urls import (
    path,
    include,
    re_path,
)
from books.views import ImportBooks, BookViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('books', BookViewSet)

app_name = "books"

urlpatterns = [
    path('', include(router.urls)),
    re_path('import_book/',
            ImportBooks.as_view(), name='import_book')
]
