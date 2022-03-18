from django.urls import path
from .views import BookDetailsView, AuthorBookView, AuthorBookCountView


urlpatterns = [
    path("book-details/", BookDetailsView.as_view(), name="book-details"),
    path("author-books/", AuthorBookView.as_view(), name="author-books"),
    path("author-books-count/",
         AuthorBookCountView.as_view(), name="author-books-count"),
]
