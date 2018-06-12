from django.contrib import admin

# Register your models here.
from books.models import Book, Genre


class GenreModelAdmin(admin.ModelAdmin):
    list_display = ["subject"]
    search_fields = ["subject"]

    class Meta:
        model = Genre


class BookModelAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "publish_date"]
    list_display_links = ["name"]
    list_filter = ["publish_date"]

    search_fields = ["name", "description", "author"]

    class Meta:
        model = Book


admin.site.register(Book, BookModelAdmin)
admin.site.register(Genre, GenreModelAdmin)
