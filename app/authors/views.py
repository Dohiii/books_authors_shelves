# Create your views here.

from rest_framework import viewsets
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

    def create(self, request, *args, **kwargs):
        """First check if Author already exist, if so, send response 409"""
        if Author.custom_objects.is_author_exist(request.data['name']):
            return Response({'error': 'Author already exist'}, status=409)
        """If author does not exist, one are created with a status.code 201"""
        super().create(request, *args, **kwargs)
        return Response({'success': 'Author created'}, status=201)

    def update(self, request, *args, **kwargs):
        if Author.custom_objects.is_author_exist(request.data['name']):
            return Response({'error': 'Author already exist'}, status=409)
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
