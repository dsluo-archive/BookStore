from django.shortcuts import render, get_object_or_404

# Create your views here.
from books.models import Book, Genre
from books.forms import MassBookForm, BookForm


def landing(request):
    return render(request, "landing.html", {})


def home(request):
    return render(request, "home_page.html", {})


def detail(request, slug):
    book = get_object_or_404(Book, slug=slug)

    return render(request, "book_detail.html", {"book": book})


def create_book(request):
    book_form = BookForm(request.POST or None, request.FILES or None)

    if book_form.is_valid():
        form_genres = book_form.cleaned_data['subject'].split(",")
        genres = []

        for genre_detail in form_genres:
            genres.append(Genre.objects.all().filter(subjects=genre_detail.strip()).first())

        if len(genres) > 0:
            new_book = book_form.save()

            for genre_detail in genres:
                new_book.subjects.add(genre_detail)

            new_book.save()

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
