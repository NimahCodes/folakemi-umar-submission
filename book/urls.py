from django.urls import path
from .views import BookDetailsView
# from .views import AuthorView

urlpatterns = [
    path('api/v1/book-details/', BookDetailsView.as_view(), name='book-details'),
    # path('api/v1/author/', AuthorView.as_view(), name='author'),
]  