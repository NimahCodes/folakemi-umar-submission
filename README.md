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
Describe in your own words what is GIL in python, and the pros and cons of it.

## Answer
```
GIL in python, the pros and cons of it

GIL is an abbreviation for Global Interpreter Lock. GIL in python is a concept that allows python to run as a single-threaded language. By default, python is a single-threaded as well as a multiple-threaded language. However, the GIL in python helps to ensure that only one thread is executed at any point in time, even in a multi-threaded architecture. This is achieved by locking other interfaces for executing the multiple threads.

Pros:

The concept of GIL makes memory management efficient in python. In Python, every object created has a reference count variable that keeps track of the number of references that point to the object. When the reference count reaches zero, the memory occupied by the object is released.

GIL prevents memory leakage in python as it does not support the execution of multi-threading architecture.

It’s a simple design as only one lock has to be managed

GIL also provides a performance boost to the single-threaded programs

It makes it possible to integrate many C libraries with Python. Which is a main reason why python is  popular.
 
Cons:

GIL restricts parallel programming and reduces efficiency.


```
## Question 2: 
Write a decorator in python that will count how many times the decorated function was called. It should print the number every time the decorated function is executed. Each function should be counted separately.

## Answer

<div>
<img src="https://res.cloudinary.com/neemathec/image/upload/v1647554051/Screenshot_2022-03-17_at_22.54.02_de4idr.png" width="100%">
</div>
```

## Question 3
If you see that a SQL SELECT query is slow - what would you do to improve it?

## Answer
```
Several reasons could be responsible for a slow SQL SELECT query operation. In troubleshooting, I will do the following:
Explicitly declare the column (or/and) row where necessary, just in case the wildcard (*) was used.

Precisely declare the SELECT ID instead of the SELECT DISTINCT command.

Check to ensure that queries are not being run in a loop or if possible, bulk insert and update data.

Carefully use clustered indexes as this helps to retrieve data faster and reduce runtime.

```



## Question 4
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
    author = serializers.ReadOnlyField(source="author.name")

    class Meta:
        model = Book
        fields = ("title", "author")

- View
class BookDetailsView(generics.CreateAPIView):
    queryset = Book.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = AuthorBookSerializers

    def get(self, request, *args, **kwargs):
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

#### Endpoint: https://book-record-api.herokuapp.com/api/v1/book-details/
[See codes](https://github.com/NimahCodes/folakemi-umar-submission/blob/main/book/views.py)


## Write another function that will print the author’s name and all the books he wrote. For all the authors we have in the database. Like this:

Leo Tolstoy: “War and Peace”, “Anna Karenina”, “Resurrection”
Alexandre Dumas: “The Three Musketeers”, “The Count of Monte Cristo”

## Answers
```
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
                           .values_list("title", flat=True).distinct()
                           }, Author.objects.values("name")
            ))
            return Response(
                dict(message="success", data=result, error=None), status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                dict(message="failed", data=None, error=f'{e}'), status=status.HTTP_400_BAD_REQUEST
            )
```
#### Endpoint: https://book-record-api.herokuapp.com/api/v1/author-books/
[See codes](https://github.com/NimahCodes/folakemi-umar-submission/blob/main/book/views.py)


## Question 4.2
4 Implement the third function, it should print the author’s name and the number of books he wrote. Order by the number of books written, descending. Like this:

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

#### Endpoint: https://book-record-api.herokuapp.com/api/v1/author-books-count/
[See codes](https://github.com/NimahCodes/folakemi-umar-submission/blob/main/book/views.py)

## Question 5
 Differences between “arrow” and “traditional” functions in javascript:

## Answer
```
Function syntax:
The traditional javascript function declaration is prefixed by the function  keyword followed by the variable, then parenthesis (with or without argument), before the curly braces, the syntax structure of arrow function is relatively pretty straightforward


Use of Duplicate named parameters:
In non-restrict mode, traditional functions allow us to use duplicate named parameters. But in strict mode, it is not allowed.
```
<div>
<img src="https://res.cloudinary.com/neemathec/image/upload/v1647534616/Screenshot_2022-03-17_at_17.30.10_txo71a.png" width="100%">
</div>

```
Whereas, in arrow functions, parameters with the same name are not allowed whether the strict mode is enabled or not.
```
<div>
<img src="https://res.cloudinary.com/neemathec/image/upload/v1647534634/Screenshot_2022-03-17_at_17.30.30_ly2t58.png" width="100%">
</div>

```
Prototype:
We can get a prototype for a traditional function, but the arrow function does not have a prototype.
```
<div>
<img src="https://res.cloudinary.com/neemathec/image/upload/v1647534645/Screenshot_2022-03-17_at_17.30.41_zujtx9.png" width="100%">
</div>

```
this:
In a traditional function, its internal “this” value is dynamic, it depends on how the function is invoked.
```
<div>
<img src="https://res.cloudinary.com/neemathec/image/upload/v1647535061/Screenshot_2022-03-17_at_17.37.35_vm6zvm.png" width="100%">
</div>

```
In the arrow function, there is no “this”, if we access this in the arrow function it will return the “this” of the closest non-arrow parent function.
```
<div>
<img src="https://res.cloudinary.com/neemathec/image/upload/v1647535109/Screenshot_2022-03-17_at_17.38.23_vc0iie.png" width="100%">
</div>

```
Use of “new” keyword:
We can use the “new” keyword on the traditional function to create a new object.
```
<div>
<img src="https://res.cloudinary.com/neemathec/image/upload/v1647535161/Screenshot_2022-03-17_at_17.39.16_wavoja.png" width="100%">
</div>

```
But arrow functions cannot be called with “new”.
```
<div>
<img src="https://res.cloudinary.com/neemathec/image/upload/v1647535213/Screenshot_2022-03-17_at_17.40.07_x3cw9f.png" width="100%">
</div>




## Question 6
React component showing number of clicks on it’s button

## Answer
```
Import React from ‘react’
 
function App() {
const [counter, setCounter] = React.useState(0)
const btnStyle ={
   margin: '200px 500px',
   width: '300px',
   fontSize: '28px',
   height: '100px',
   color: '#FFFFFF',
   backgroundColor: '#E5E5E5',
   borderRadius: '5px',
  }
return (
  <div className="App">
   <button onClick={() => setCounter(counter + 1)} style={btnStyle}>
     Click count: {counter}
   </button>
  </div>
);
}

export default App;
```
