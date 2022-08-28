from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from shelves.models import Shelf
from shelves.serializers import (
    ShelfSerializer,
    ShelfAddBookSerializer)


class ListPublicShelves(generics.ListAPIView):
    """List of public Shelves"""
    queryset = Shelf.objects.filter(access='PUBLIC')
    serializer_class = ShelfSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]


class ShelfViewSet(viewsets.ModelViewSet):
    """Main View for Shelf Logic"""
    queryset = Shelf.objects.all()
    serializer_class = ShelfSerializer
    authentication_classes = [JWTAuthentication]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return Shelf.objects.filter(user=self.request.user.profile)

    def perform_create(self, serializer):
        """Create new shelf"""
        serializer.save(user=self.request.user.profile)


class ShelfAddBook(viewsets.ModelViewSet):
    """Add book to shelf view set, only PATCH"""
    queryset = Shelf.objects.all()
    serializer_class = ShelfAddBookSerializer
    authentication_classes = [JWTAuthentication]
    http_method_names = ['patch']

    def get_queryset(self):
        return Shelf.objects.filter(user=self.request.user.profile)

    # def update(self, request, *args, **kwargs):
    #     print('It was patched')
    #     print(request.data)
    #     return self.partial_update(request, *args, **kwargs)
