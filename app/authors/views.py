# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from authors.models import Author
from authors.serializers import AuthorSerializer
from view_helpers.authors_helpers import import_author_from_wiki


class ImportAuthor(APIView):
    def put(self, request):
        return import_author_from_wiki(request)

# class ImportAuthorAndBooks(APIView):
#     def put(self, request):
#         try:
#             import_author_from_wiki(request)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        """First check if Author already exist, if so, send response 409"""
        if Author.custom_objects.is_author_exist(request.data['name']):
            return Response({'error': 'Author already exist'}, status=409)
        """If author does not exist, we are creating one with a status code 201"""
        super().create(request, *args, **kwargs)
        return Response({'success': 'Author created'}, status=201)

