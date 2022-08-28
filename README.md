My pet project, CRUD application, you can import books by author name, and import authors from wikipedia.
It is possible to make bookshelves collections, 3 shelf are there by default on user creation.

![9318](https://user-images.githubusercontent.com/77291884/165365277-c0d2b989-42be-4a75-8907-ca39e050263a.png)


# Endpoints

## Users:

**POST** Register/Create User (**NO Auth**) `/api/v1/register/`
example payload:
```
{
    "email": [email:unique],
    "password": [string],
    "name": [string]
}
```

**POST** Login with user (**Auth**) `/api/v1/login/`
example payload:
```
{
    "email": [email],
    "password": [string],
}
```
expected status: `200 OK`

expected body:
`
{
    "refresh": [token],
    "access": [token]
}
`
**GET** logged-in user (**Auth**) `/api/v1/user_me/`

Expected status code :`200 OK`



## Profiles:

*Profile get created automatically as user got created and is used as owner for Authors/Books/Shelves created by user*

**GET** all profiles (**Auth**) `/api/v1/profiles/`

Expected status code :`200 OK`

**GET** my profile need to be logged in no id needed (**Auth**) `/api/v1/profile/`

Expected status code :`200 OK`

**PATCH** no id needed (**Auth**) `/api/v1/profile/`

#### Payload example (multiple books added):
```
{
    "username": [string],
}
```

Expected status code :`200 OK`

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

## Import author:

User can import Authors from Wiki API by Authors name.
Possible that import will be incorrect by importing wrong article related to author.

**PUT** single author (**Auth**)`/api/v1/import_author/`

Payload example:
```
{
    "name": [string:unique]
}
```

Expected status code :`201 Created`

*"invalid": "Author with this name already exist"*

Expected status code :`400 Bad Request`

## Books:
**GET** all books (**No Auth**) `/api/v1/books/`

Expected status code :`200 OK`

**GET** single book (**No Auth**) `/api/v1/books/{id}`

Expected status code :`200 OK`

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


## Import books:

User can import book infor from Google API by authors name

**PUT** multiple books by author name (**Auth**)`/api/v1/import_book/`

Payload example:
```
{
    "name": [string:unique]
}
```

Expected response `{"imported": [int]}`

Expected status code :`201 Created`

*"invalid": "Author with this name already exist"*

*"invalid": "Book with this external id already exist"*

Expected status code :`400 Bad Request`





## Shelves:

**GET** all public shelves (**Auth**) `/api/v1/shelves_public/`

Expected status code :`200 OK`

**GET** all users shelves (needs to be logged in) (**Auth**) `/api/v1/shelves/`

Expected status code :`200 OK`

**GET** single shelf (**Auth**) `/api/v1/shelves/{id}`

Expected status code :`200 OK`

**PATCH** update shelf (**Auth**) `/api/v1/shelves/{id}`

Expected status code :`200 OK`

**POST** single book (**Auth**)`/api/v1/shelves/`

Payload example:
```
{
    "shelf_name": [string:unique],
    "description": [text],
    "access": [string:choise "PUBLIC" or "PRIVATE"]
}
```

Expected status code :
`201 Created`


**DELETE** single shelf (**Auth**)`/api/v1/shelves/{id}`

Expected status  on success code :`204 No Content`

*User can delete only the shelf that he owns(add previously)*

Expected status  on fail code :`403 Forbitten` 

## Add Books to shelf(id) by book id:
`/api/v1/shelves/shelf_add/{id}`

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










Testing:

to see detailed tests and coverage report: `coverage run manage.py test -v2 && coverage report`




