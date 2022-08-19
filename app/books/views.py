from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
    )
from .filters import BooksFilter
from books.models import Book
from .serializers import BookSerializer
from rest_framework import viewsets, permissions
from rest_framework import generics
from view_helpers.books_helpers import import_book_by_author
from authors.serializers import AuthorSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication


class ImportBooks(generics.GenericAPIView):
    # permission_classes = [permissions.IsAdminUser]
    serializer_class = AuthorSerializer
    authentication_classes = [JWTAuthentication]

    def put(self, request):
        return import_book_by_author(request)

    def perform_create(self, serializer):
        """Create new recipe"""
        serializer.save(user=self.request.user)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_class = BooksFilter
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Create new recipe"""
        serializer.save()
