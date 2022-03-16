from rest_framework import serializers
from .models import Book
from .models import Author


class BookSerializers(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["name",]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["title", "author",]        
