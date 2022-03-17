from rest_framework import serializers
from .models import Book
from .models import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('name',)


class BookSerializers(serializers.ModelSerializer):
    author = AuthorSerializer(many=False)

    class Meta:
        model = Book
        fields = "__all__"


class AuthorBookSerializers(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')

    class Meta:
        model = Book
        fields = ('title', 'author')
