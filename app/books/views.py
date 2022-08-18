from .filters import BooksFilter
from books.models import Book
from .serializers import BookSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from view_helpers.books_helpers import import_book_by_author


class ImportBooks(APIView):
    def put(self, request):
        return import_book_by_author(request)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_class = BooksFilter
