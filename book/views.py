from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Author, Book
from .serializers import AuthorBookSerializers


class BookDetailsView(generics.CreateAPIView):
    queryset = Book.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = AuthorBookSerializers

    def get(self, request, *args, **kwargs):
        try:
            book_author = self.serializer_class(
                Book.objects.select_related("author").all(),  many=True).data

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
        try:
            result = list(map(
                lambda d: {Author.objects.get(name=d.get("name")).name:
                           Book.objects.filter(
                               author=Author.objects.get(name=d.get("name")))
                           .values_list('title', flat=True).distinct()
                           }, Author.objects.values("name")
            ))
            return Response(
                dict(message="success", data=result, error=None),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                dict(message="failed", data=None, error=f'{e}'),
                status=status.HTTP_400_BAD_REQUEST
            )


class AuthorBookCountView(generics.CreateAPIView):
    queryset = Book.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = AuthorBookSerializers

    def get(self, request, *args, **kwargs):
        try:
            result = list(map(
                lambda d: {Author.objects.get(name=d.get("name")).name:
                           len(Book.objects.filter(
                               author=Author.objects.get(name=d.get("name")))
                           .values_list("title", flat=True).distinct())
                           }, Author.objects.values('name')
            ))
            return Response(
                dict(message="success", data=result, error=None),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                dict(message="failed", data=None, error=f'{e}'),
                status=status.HTTP_400_BAD_REQUEST
            )
