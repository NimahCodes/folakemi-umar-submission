# from rest_framework import serializer
# from rest_framework.generics import GenericAPIView
# from rest_framework.response import Response
# from django.http import HttpResponse
# from .models import Author
# from .models import Book
# from .serializers import BookSerializer
# from .serializers import AuthorSerializer


# def print_books(request):
#     permission_class=["AllowAny",]
#     if request.method == "GET":
#         books = Book.objects.all()
#         serializer = BookSerializer(books, data=request.data)
#         for book in books:
#             return Response({"data":{
#                 "title": book.title,
#                 "author_name": book.author.name}
#             }
#         )


# def authors_books(request):
#     permission_class=['AllowAny',]
#     if request.method == 'GET':
#     query = Author.objects.values('author__name')\
#    .annotate(c=Count('title'))
#     for i in query:       
#        me = Author.objects.filter(author__name=i.get('author__name'))\
#            .values_list('title', flat=True)
#        print(f"{i.get('author__name')}:  {', '.join(map(str, me))}")       



# class BookDetailsView(GenericAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             get_name = name = serializer.validated_data["name"]
#             new_receipt = Receipt.objects.create(
#                 user=request.user,
#                 name=get_name,
#                 address=serializer.validated_data["address"],
#                 phone_number=serializer.validated_data["phone_number"],
#                 total_amount_payable=serializer.validated_data["total_amount_payable"],
#             )

#             receipt = generate_receipt(
#                 serializer.validated_data["name"],
#                 serializer.validated_data["address"],
#                 serializer.validated_data["phone_number"],
#                 serializer.validated_data["total_amount_payable"],
#                 serializer.validated_data["description"],
#                 new_receipt.id,
#             )
#             if receipt is not None:
#                 response = HttpResponse(
#                     open(f"{get_name}_receipt.pdf", "rb").read(),
#                     content_type="application/pdf",
#                 )
#                 response[
#                     "Content-Disposition"
#                 ] = f"attachment; filename={get_name}_receipt.pdf"
#                 return response

#             return Response(
#                 dict(error=f"{serializer.error}"), status=status.HTTP_400_BAD_
#             )


# class AuthorView(GenericAPIView):
    
