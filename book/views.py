import functools
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Author, Book
from .serializers import BookSerializers, AuthorBookSerializers
from itertools import groupby


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
                dict(message="failed", data=None, error=f'{e}'), status=status.HTTP_400_BAD_REQUEST
            )


class AuthorBookView(generics.CreateAPIView):
    queryset = Book.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = AuthorBookSerializers

    def get(self, request, *args, **kwargs):
        '''
        4.2 Write another function that will print the author’s 
        name and all the books he wrote. For all the authors 
        we have in the database. Like this:
        Leo Tolstoy: “War and Peace”, “Anna Karenina”, “Resurrection”
        Alexandre Dumas: “The Three Musketeers”, “The Count of Monte Cristo”
        '''
        try:
            result = list(map(
                lambda d: {Author.objects.get(name=d.get("name")).name:
                           Book.objects.filter(
                               author=Author.objects.get(name=d.get("name")))
                           .values_list('title', flat=True).distinct()
                           }, Author.objects.values('name')
            ))
            return Response(
                dict(message="success", data=result, error=None), status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                dict(message="failed", data=None, error=f'{e}'), status=status.HTTP_400_BAD_REQUEST
            )


class AuthorBookCountView(generics.CreateAPIView):
    queryset = Book.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = AuthorBookSerializers

    def get(self, request, *args, **kwargs):
        '''
        4.3 Implement the third function, it should print 
        the author’s name and the number of books he wrote. 
        Order by the number of books written, descending. Like this:
        Leo Tolstoy: 3
        Alexandre Dumas: 2
        '''
        try:
            result = list(map(
                lambda d: {Author.objects.get(name=d.get("name")).name:
                           len(Book.objects.filter(
                               author=Author.objects.get(name=d.get("name")))
                           .values_list('title', flat=True).distinct())
                           }, Author.objects.values('name')
            ))
            return Response(
                dict(message="success", data=result, error=None), status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                dict(message="failed", data=None, error=f'{e}'), status=status.HTTP_400_BAD_REQUEST
            )
