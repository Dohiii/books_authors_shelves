My pet project, CRUD application, you can import books by author name, and import authors from wikipedia.
It is possible to make bookshelves collections, 3 shelf are there by default on user creation.

![9318](https://user-images.githubusercontent.com/77291884/165365277-c0d2b989-42be-4a75-8907-ca39e050263a.png)


# Endpoints

## Authors:
**GET** all books (**No Auth**) `/api/v1/authors/`

**GET** single book (**No Auth**) `/api/v1/authors/{id}`

**POST** single book (**Auth**)`/api/v1/authors/`

Payload example:
```
 {
    "name": [string:unique],
    "wiki_url": [url]
}
```

Expected status code :
`201 Created`

**PUT** single author (**Auth**)`/api/v1/authors/{id}`

Expected status code :`200 OK`

**PATCH** single author (**Auth**)`/api/v1/authors/{id}`

Expected status code :`200 OK`

**DELETE** single author (**Auth**)`/api/v1/authors/{id}`

Expected status  on success code :`204 No Content`

*User can delete only the author that he owns(add previously)*

Expected status  on fail code :`403 Forbitten` 







## Books:
**GET** all books (**No Auth**) `/api/v1/books/`

**GET** single book (**No Auth**) `/api/v1/books/{id}`

**POST** single book (**Auth**)`/api/v1/books/`

Payload example (book with multiple authors POST):
```
 {
        "external_id": [string:unique],
        "title": [string],
        "authors": [
            {
                "name": [string:unique]
            },
            {
                "name": [string:unique]
            },
            ...
        ],
        "published_year": [string],
        "acquired": [Bool],
        "thumbnail": [string]
    }
```

Expected status code :
`201 Created`

**PUT** single book (**Auth**)`/api/v1/books/{id}`

Expected status code :`200 OK`

**PATCH** single book (**Auth**)`/api/v1/books/{id}`

Expected status code :`200 OK`

**DELETE** single book (**Auth**)`/api/v1/books/{id}`

Expected status  on success code :`204 No Content`

*User can delete only the book that he owns(add previously)*

Expected status  on fail code :`403 Forbitten` 










## Shelves:

add books to shelf(id) by book id:
`/api/v1/shelves/shelf_add/`

#### Payload example (multiple books added):
```
{
    "books": [
        {
        "book_id": [book_id]
        },
        {
        "book_id": [book_id]
        },
        .....
    ]
}
```




Testing: <br>
to see detailed tests and coverage report: coverage run manage.py test -v2 && coverage report




