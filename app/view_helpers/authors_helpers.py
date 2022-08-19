from rest_framework import status
from rest_framework.response import Response
import wikipedia
from wikipedia.exceptions import DisambiguationError

from authors.models import Author
from authors.serializers import AuthorSerializer


def import_author_from_wiki(request):
    try:
        page = wikipedia.page(f"{request.data['name']}(authors_writers)")
        if page is not None:
            title = page.title
            wiki_url = page.url

            payload = {
                'name': title,
                'wiki_url': wiki_url,
            }

            if Author.custom_objects.is_author_exist(title):
                return Response({'error': 'Author already exist'}, status=409)
            else:
                serializer = AuthorSerializer(data=payload)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,
                                    status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    except DisambiguationError:
        return Response({'error': 'Please try another name'})


def import_author_and_books(request):
    try:
        page = wikipedia.page(f"{request.data['name']}(authors_writers)")
        if page is not None:
            title = page.title
            wiki_url = page.url

            payload = {
                'name': title,
                'wiki_url': wiki_url,
            }

            if Author.custom_objects.is_author_exist(title):
                return Response({'error': 'Author already exist'}, status=409)
            else:
                serializer = AuthorSerializer(data=payload)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,
                                    status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    except DisambiguationError:
        return Response({'error': 'Please try another name'})
