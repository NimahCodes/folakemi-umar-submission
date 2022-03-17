from django.urls import path
from .views import BookDetailsView, AuthorBookView, AuthorBookCountView
# from .views import AuthorView

urlpatterns = [
    path('api/v1/book-details/', BookDetailsView.as_view(), name='book-details'),
    path('api/v1/author-books/', AuthorBookView.as_view(), name='author-books'),
    path('api/v1/author-books-count/',
         AuthorBookCountView.as_view(), name='author-books-count'),
    # path('api/v1/author/', AuthorView.as_view(), name='author'),
]
