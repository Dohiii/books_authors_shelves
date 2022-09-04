import json
import requests
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response

from authors.models import Author
from books.models import Book


def import_book_by_author(request):
    url = 'https://www.googleapis.com/books/v1/volumes?q=inauthor'
    imported = 0
    author = request.data['name']
    api_url = f"{url}:{str(author)}"
    res = requests.get(api_url)
    json_data = json.loads(res.text)
    try:
        books_data = json_data['items']
        for i, book in enumerate(books_data):

            title = book["volumeInfo"]["title"]
            external_id = book["id"]
            thumbnail = book["volumeInfo"]["previewLink"]
            pages = book["volumeInfo"]["pageCount"]
            published_year = book["volumeInfo"]["publishedDate"][0:4]
            payload = {
                'title': title,
                'external_id': external_id,
                'thumbnail': thumbnail,
                'pages': int(pages),
                'published_year': published_year
            }
            if not Book.objects.filter(external_id=external_id).exists():
                Book.objects.create(user=request.user.profile, **payload)
                imported += 1

                book = Book.objects.filter(external_id=external_id).first()

                authors = []

                for author in books_data[i]["volumeInfo"]["authors"]:
                    try:
                        author_data = Author.objects.create(
                            name=author,
                            user=request.user.profile)
                        authors.append(author_data)
                    except IntegrityError:
                        author_data = Author.objects.\
                            filter(name=author).first()
                        authors.append(author_data)

                book.authors.set(authors)

                continue

    except KeyError:
        return Response({"invalid": "Author with this name does not exist"},
                        status=status.HTTP_400_BAD_REQUEST
                        )

    return Response({"imported": imported})
