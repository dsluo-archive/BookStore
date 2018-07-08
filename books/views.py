from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.db.models import Q


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
    queryset_list = Book.objects.all().order_by("name")

    book_name = request.GET.get('name')
    book_author = request.GET.get('author')
    book_isbn = request.GET.get('isbn')
    book_genre = request.GET.get('genre')

    if book_name:
        book_name = book_name.split('%')
        for name in book_name:
            queryset_list = queryset_list.filter(name__contains=name)
    if book_author:
        book_author = book_author.split('%')
        for author in book_author:
            queryset_list = queryset_list.filter(author__name=author)
    if book_isbn:
        book_isbn = book_isbn.split('%')
        for isbn in book_isbn:
            queryset_list = queryset_list.filter(isbn=isbn)
    if book_genre:
        book_genre = book_genre.split('%')
        for genre in book_genre:
            queryset_list = queryset_list.filter(subjects__subjects=genre)

    return render(request, "query.html", {"books": queryset_list})


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
