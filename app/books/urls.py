from django.urls import re_path
from books.views import ImportBooks

app_name = "import_book"

urlpatterns = [
    re_path('import_book/', ImportBooks.as_view(), name='import_book')
]