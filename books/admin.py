from django.contrib import admin

# Register your models here.
from books.models import Author, Book, Genre


class GenreModelAdmin(admin.ModelAdmin):
    list_display = ["subjects"]
    search_fields = ["subjects"]

    class Meta:
        model = Genre


class AuthorModelAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]

    class Meta:
        model = Author


class BookModelAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "publish_date"]
    list_display_links = ["name"]
    list_filter = ["publish_date"]

    search_fields = ["name", "description", "author"]

    class Meta:
        model = Book


admin.site.register(Book, BookModelAdmin)
admin.site.register(Genre, GenreModelAdmin)
admin.site.register(Author, AuthorModelAdmin)
