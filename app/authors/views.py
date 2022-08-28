# Create your views here.
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
    )
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from authors.models import Author
from authors.serializers import AuthorSerializer
from view_helpers.authors_helpers import import_author_from_wiki
from rest_framework import generics


class ImportAuthor(generics.GenericAPIView):
    # permission_classes = [permissions.IsAdminUser]
    serializer_class = AuthorSerializer
    authentication_classes = [JWTAuthentication]

    def put(self, request):
        return import_author_from_wiki(request)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    authentication_classes = [JWTAuthentication]

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
