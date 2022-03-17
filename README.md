# folakemi-umar-submission

## Technologies leveraged for this project includes 

- [Python 3.9](https://python.org) : Base programming language for development
- [PostgreSQL](https://www.postgresql.org/) : Application relational databases for development, staging and production environments
- [Django Framework](https://www.djangoproject.com/) : Development framework used for the application
- [Django Rest Framework](https://www.django-rest-framework.org/) : Provides API development tools for easy API development
- [Github](https://docs.github.com/en/free-pro-team@latest/actions) : Code repository, Management and deployment 


## How to run the application
- clone the repository `git clone https://github.com/NimahCodes/folakemi-umar-submission.git`
- Change directory `cd folakemi-umar-submission`
- create a virtual environment `python -m venv <virtual environment name>`
- activate virtual environment `<virtual environment name>/bin/activate`
- install requirements `pip install -r requirements.txt`
- make migration `python manage.py makemigrations`
- migrate `python manage.py migrate`
- run the server `python manage.py runserver`
- create super user `python manage.py createsuperuser`
- open the the running app on your browser `http://127.0.0.1:8001/api/v1/book-details/`

## lists of endpoints:
LocalHost 
- http://127.0.0.1:8001/api/v1/book-details/
- http://127.0.0.1:8001/api/v1/author-books/
- http://127.0.0.1:8001/api/v1/author-books-count/

Live host
-  https://book-record-api.herokuapp.com/api/v1/book-details/
-  https://book-record-api.herokuapp.com/api/v1/author-books/
-  https://book-record-api.herokuapp.com/api/v1/author-books-count/



## Question 1
Assume we have ~100 books and ~25 authors in our database.
Try to write efficient queries, keep in mind how many requests the ORM can make to the database.

4.1 Using Django ORM, write a function that will print the book title and the author name (who wrote it) for all the books we have in the database. Like this:

“War and Peace”. Leo Tolstoy
“Anna Karenina”. Leo Tolstoy
“Resurrection”. Leo Tolstoy
“The Three Musketeers”. Alexandre Dumas
“The Count of Monte Cristo”. Alexandre Dumas


## Answers
```
- Serializer
class AuthorBookSerializers(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')

    class Meta:
        model = Book
        fields = ('title', 'author')

- View
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
```

## Endpoint: https://book-record-api.herokuapp.com/api/v1/book-details/



## Question 2
4.2 Write another function that will print the author’s name and all the books he wrote. For all the authors we have in the database. Like this:

Leo Tolstoy: “War and Peace”, “Anna Karenina”, “Resurrection”
Alexandre Dumas: “The Three Musketeers”, “The Count of Monte Cristo”

## Answers
```
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
```
## Endpoint: https://book-record-api.herokuapp.com/api/v1/author-books/



## Question 3
4.3 Implement the third function, it should print the author’s name and the number of books he wrote. Order by the number of books written, descending. Like this:

Leo Tolstoy: 3
Alexandre Dumas: 2

## Answers
```
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

```

## Endpoint: https://book-record-api.herokuapp.com/api/v1/author-books-count/

[See codes](https://github.com/NimahCodes/folakemi-umar-submission/blob/main/book/views.py)