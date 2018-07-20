from django import forms

from books.models import Book


class MassBookForm(forms.Form):
    file = forms.FileField()


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            "item_picture",
            "name",
            "isbn",
            "publisher",
            "price",
            "author",
            "publish_date",
            "count_in_stock",
            "description",
            "subjects",
        ]