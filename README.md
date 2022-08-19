My pet project, CRUD application, you can import books by author name, and import authors from wikipedia.


Endpoints:
/api/v1/register/ # no auth required
/api/v1/login/ # Created user required
/admin/ # Admin user required
/schema/ # no auth required
/api/v1/books/ # no auth required for get, required for POST PUT DELETE PATCH
/api/v1/authors/ # no auth required for get, required for POST PUT DELETE PATCH
/api/v1/user_me/ # auth required for all actions
/api/v1/import_author/ # no auth required for get, required for POST PUT DELETE PATCH
/api/v1/import_books/ # no auth required for get, required for POST PUT DELETE PATCH




