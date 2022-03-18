from django.contrib import admin
from .models import Book, Author

# Author admin interface
admin.site.register(Author)

# Book admin interface
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):   
    list_display = (
        "title", "author",
    )
