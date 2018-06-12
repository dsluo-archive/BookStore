from django.shortcuts import render

# Create your views here.
from books.models import Book, Genre
from books.forms import MassBookForm, BookForm


def landing(request):
    return render(request, "landing.html", {})


def home(request):
    return render(request, "home_page.html", {})


def detail(request, slug):
    return render(request, "book_detail.html", {"slug": slug})


def create_book(request):
    book_form = BookForm(request.POST or None, request.FILES or None)

    if book_form.is_valid():
        genre = Genre.objects.all().filter(subject=book_form.cleaned_data['subject']).values().first()

        if genre:
            new_book = book_form.save()
            #new_book.subject.set(genre)
            #new_book.save()

            return render(request, "home_page.html", {})
        else:
            book_form.add_error('subject', "Field must be a recognized genre.")

    return render(request, "create_book.html", {"book_form": book_form})


def mass_create_book(request):
    mass_book_form = MassBookForm(request.POST or None, request.FILES or None)

    if mass_book_form.is_valid():
        return render(request, "home_page.html", {})

    return render(request, "mass_create_book.html", {"mass_book_form": mass_book_form})


def query(request):
    return render(request, "query.html", {})
