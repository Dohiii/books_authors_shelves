from rest_framework import status
from rest_framework.response import Response
import wikipedia
from wikipedia.exceptions import PageError
from authors.serializers import AuthorSerializer


def import_author_from_wiki(request):
    try:
        page = wikipedia.page(f"{request.data['name']}(person)")
        if page is not None:
            title = page.title
            wiki_url = page.url

            payload = {
                'name': title,
                'wiki_url': wiki_url,
            }
            serializer = AuthorSerializer(data=payload)
            if serializer.is_valid():
                serializer.save(user=request.user.profile)
                return Response(serializer.data,
                                status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    except PageError:
        return Response({'error': 'Please try another name'})
