from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied


# Create your views here.
from books.models import Book, Genre, Author
from books.forms import MassBookForm, BookForm


def landing(request):

    new_books = Book.objects.all().order_by("publish_date")
    newly_added_books = Book.objects.all().order_by("-id")

    return render(request, "landing.html", {"new_books": new_books,
                                            "newly_added_books": newly_added_books})


def home(request):
    new_books = Book.objects.all().order_by("publish_date")
    newly_added_books = Book.objects.all().order_by("-id")
    latest_author = Author.objects.latest("id")
    genres = Genre.objects.all()

    return render(request, "home_page.html", {"new_books": new_books,
                                              "newly_added_books": newly_added_books,
                                              "latest_author": latest_author,
                                              "genres": genres})


def all_books(request):
    return render(request, "query.html", {"books":Book.objects.all().order_by("name")})


def detail(request, slug):
    book = get_object_or_404(Book, slug=slug)

    return render(request, "book_detail.html", {"book": book})


def create_book(request):
    if request.user.is_authenticated and (request.user.member.vendor or request.user.is_staff):
        book_form = BookForm(request.POST or None, request.FILES or None)

        if book_form.is_valid():
            book_form.save()

            return render(request, "home_page.html", {})

        return render(request, "create_book.html", {"book_form": book_form})
    else:
        raise PermissionDenied


def mass_create_book(request):
    mass_book_form = MassBookForm(request.POST or None, request.FILES or None)

    if mass_book_form.is_valid():
        return render(request, "home_page.html", {})

    return render(request, "mass_create_book.html", {"mass_book_form": mass_book_form})


def query(request):
    return render(request, "query.html", {})
