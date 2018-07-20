from django import forms

from books.models import Book
from vendors.models import Vendor


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


class VendorRegistrationForm(forms.Form):
    code = forms.CharField(max_length=16, required=True)
    vendor = forms.ModelChoiceField(Vendor.objects.all(), required=True)
