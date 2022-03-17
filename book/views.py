import functools
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Author, Book
from .serializers import BookSerializers, AuthorBookSerializers
import operator


def get_title_and_author(queryset):
    items = []
    for item in queryset:
        items.append(f'"{item.title}" .{item.author.name}')


class BookDetailsView(generics.CreateAPIView):
    queryset = Book.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = AuthorBookSerializers

    def get(self, request, *args, **kwargs):
        '''
        4.1 Using Django ORM, write a function that will
        print the book title and the author name (who wrote it)
        for all the books we have in the database. Like this:
        “War and Peace”. Leo Tolstoy
        “Anna Karenina”. Leo Tolstoy
        “Resurrection”. Leo Tolstoy
        “The Three Musketeers”. Alexandre Dumas
        “The Count of Monte Cristo”. Alexandre Dumas
        '''
        try:
            book_author = self.serializer_class(
                Book.objects.select_related('author').all(),  many=True).data

            result = list(map(
                lambda d: f'“{d.get("title")}“. {d.get("author")}', book_author)
            )
            return Response(
                dict(message="success", data=result, error=None), status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                dict(message="falied", data=None, error=f'{e}'), status=status.HTTP_400_BAD_REQUEST
            )
