from django.urls import re_path
from authors.views import ImportAuthor

app_name = "import_author"

urlpatterns = [
    re_path('import_author/', ImportAuthor.as_view(), name='import_author')
]