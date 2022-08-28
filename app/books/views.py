from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
    )
from rest_framework.response import Response

from books.filters import BooksFilter
from books.models import Book
from books.serializers import BookSerializer, BookListSerializer
from rest_framework import viewsets, status
from rest_framework import generics
from view_helpers.books_helpers import import_book_by_author
from authors.serializers import AuthorSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication


class ImportBooks(generics.GenericAPIView):
    serializer_class = AuthorSerializer
    authentication_classes = [JWTAuthentication]

    def put(self, request):
        return import_book_by_author(request)

    def perform_create(self, serializer):
        """Create new recipe"""
        serializer.save(user=self.request.user)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    filterset_class = BooksFilter
    authentication_classes = [JWTAuthentication]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return BookSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Create new recipe"""
        serializer.save(user=self.request.user.profile)

    def destroy(self, request, *args, **kwargs):
        item = self.get_object()
        if item.user == self.request.user.profile:
            item.delete()
            return Response({'success': 'Item was deleted'},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({'invalid': 'You can delete only your items'},
                        status=status.HTTP_403_FORBIDDEN)
