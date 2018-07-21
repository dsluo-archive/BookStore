from django import forms

from books.models import Book, Publisher
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
            "price",
            "author",
            "publish_date",
            "count_in_stock",
            "description",
            "subjects",
        ]

    publisher = forms.CharField(max_length=120, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.publisher:
            self.fields['publisher'].initial = self.instance.publisher.name

    def save(self, commit=True):
        book = super(BookForm, self).save(commit=False)
        book.publisher, created = Publisher.objects.get_or_create(name__iexact=self.cleaned_data['publisher'])

        if created:
            book.publisher.name = self.cleaned_data['publisher']
            book.publisher.save()

        if commit:
            book.save()

        return book


class VendorRegistrationForm(forms.Form):
    code = forms.CharField(max_length=16, required=True)
    vendor = forms.ModelChoiceField(Vendor.objects.all(), required=True)
