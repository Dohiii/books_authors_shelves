My pet project, CRUD application, you can import books by author name, and import authors from wikipedia.

![9318](https://user-images.githubusercontent.com/77291884/165365277-c0d2b989-42be-4a75-8907-ca39e050263a.png)


Endpoints: <br>
/api/v1/register/ # no auth required <br>
/api/v1/login/ # Created user required <br> 
/admin/ # Admin user required <br> 
/schema/ # no auth required <br>
/api/v1/books/ # no auth required for get, required for POST PUT DELETE PATCH <br>
/api/v1/authors/ # no auth required for get, required for POST PUT DELETE PATCH <br>
/api/v1/user_me/ # auth required for all actions <br>
/api/v1/import_author/ # no auth required for get, required for POST PUT DELETE PATCH <br>
/api/v1/import_books/ # no auth required for get, required for POST PUT DELETE PATCH <br>


Testing: <br>
to see detailed tests and coverage report: coverage run manage.py test -v2 && coverage report




