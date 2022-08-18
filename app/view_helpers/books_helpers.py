import json

import requests
from rest_framework import status
from rest_framework.response import Response

from authors.models import Author
from books.models import Book
from books.serializers import BookSerializer


def import_book_by_author(request):
    url = 'https://www.googleapis.com/books/v1/volumes?q=inauthor'
    imported = 0
    author = request.data['name']
    api_url = f"{url}:{str(author)}"
    res = requests.get(api_url, timeout=1)
    json_data = json.loads(res.text)
    try:
        books_data = json_data['items']
        for i, book in enumerate(books_data):

            authors = []
            title = book["volumeInfo"]["title"]
            external_id = book["id"]
            thumbnail = book["volumeInfo"]["previewLink"]
            pages = book["volumeInfo"]["pageCount"]
            published_year = book["volumeInfo"]["publishedDate"][0:4]

            for author in books_data[i]["volumeInfo"]["authors"]:
                author_object, created = Author.objects.get_or_create(name=author)
                authors.append(author_object.__dict__)

            payload = {
                'authors': authors,
                'title': title,
                'external_id': external_id,
                'thumbnail': thumbnail,
                'pages': int(pages),
                'published_year': published_year
            }
            if not Book.objects.filter(external_id=external_id).exists():
                serializer = BookSerializer(data=payload)
                if serializer.is_valid():
                    serializer.save()
                    imported += 1
                    continue
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                continue

    except KeyError:
        return Response({"message": "Sorry, but this Author does not exist"})

    return Response({"imported": imported})
