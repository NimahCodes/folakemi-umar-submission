from django.db import models


class Author(models.Model):
    '''
    author model class
    '''
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Book(models.Model):
    '''
    book model class
    '''
    title = models.CharField(max_length=100)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"
